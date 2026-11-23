from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.extensions import db
from app.models.user import User
from app.models.cart import Cart
from app.utils.validators import validate_email, validate_phone, clean_phone, validate_password_strength

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    
    full_name = data.get('full_name', '').strip()
    email = data.get('email', '').strip().lower()
    phone = data.get('phone', '').strip() if data.get('phone') else None
    password = data.get('password', '')
    confirm_password = data.get('confirm_password', '')

    # Validations
    if not full_name:
        return jsonify({'success': False, 'message': 'Full name is required.'}), 400

    if not validate_email(email):
        return jsonify({'success': False, 'message': 'Please provide a valid email address.'}), 400

    if phone and not validate_phone(phone):
        return jsonify({'success': False, 'message': 'Please provide a valid 10-digit mobile number.'}), 400

    is_strong, pwd_err = validate_password_strength(password)
    if not is_strong:
        return jsonify({'success': False, 'message': pwd_err}), 400

    if confirm_password and password != confirm_password:
        return jsonify({'success': False, 'message': 'Passwords do not match.'}), 400

    # Duplicate check
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'success': False, 'message': 'An account with this email already exists.'}), 409

    # Create user
    user = User(
        full_name=full_name,
        email=email,
        phone=clean_phone(phone),
        role='customer',
        is_active=True
    )
    user.set_password(password)
    db.session.add(user)
    db.session.flush()

    # Create user cart
    cart = Cart(user_id=user.id)
    db.session.add(cart)
    db.session.commit()

    # Issue JWT token
    token = create_access_token(identity=str(user.id))

    return jsonify({
        'success': True,
        'message': 'Account created successfully.',
        'access_token': token,
        'user': user.to_dict()
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password are required.'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'success': False, 'message': 'Invalid email or password.'}), 401

    if not user.is_active:
        return jsonify({'success': False, 'message': 'Account has been deactivated. Please contact support.'}), 403

    # Ensure user has a cart
    if not user.cart:
        cart = Cart(user_id=user.id)
        db.session.add(cart)
        db.session.commit()

    token = create_access_token(identity=str(user.id))

    return jsonify({
        'success': True,
        'message': 'Logged in successfully.',
        'access_token': token,
        'user': user.to_dict()
    }), 200


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'success': False, 'message': 'User not found.'}), 404

    return jsonify({
        'success': True,
        'user': user.to_dict()
    }), 200


@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'message': 'User not found.'}), 404

    data = request.get_json() or {}
    if 'full_name' in data and data['full_name'].strip():
        user.full_name = data['full_name'].strip()
    
    if 'phone' in data:
        p = data['phone']
        if p and not validate_phone(p):
            return jsonify({'success': False, 'message': 'Invalid mobile number format.'}), 400
        user.phone = clean_phone(p)

    db.session.commit()
    return jsonify({
        'success': True,
        'message': 'Profile updated successfully.',
        'user': user.to_dict()
    }), 200


@auth_bp.route('/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'message': 'User not found.'}), 404

    data = request.get_json() or {}
    old_password = data.get('old_password', '')
    new_password = data.get('new_password', '')

    if not user.check_password(old_password):
        return jsonify({'success': False, 'message': 'Incorrect current password.'}), 400

    is_strong, pwd_err = validate_password_strength(new_password)
    if not is_strong:
        return jsonify({'success': False, 'message': pwd_err}), 400

    user.set_password(new_password)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Password changed successfully.'
    }), 200


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({
        'success': True,
        'message': 'Successfully logged out.'
    }), 200
