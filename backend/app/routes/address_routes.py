from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.address import Address
from app.utils.validators import validate_phone, clean_phone, validate_pincode

address_bp = Blueprint('addresses', __name__, url_prefix='/api/addresses')

@address_bp.route('', methods=['GET'])
@jwt_required()
def get_addresses():
    user_id = int(get_jwt_identity())
    addresses = Address.query.filter_by(user_id=user_id).order_by(Address.is_default.desc(), Address.id.desc()).all()
    return jsonify({
        'success': True,
        'count': len(addresses),
        'addresses': [addr.to_dict() for addr in addresses]
    }), 200


@address_bp.route('', methods=['POST'])
@jwt_required()
def add_address():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}

    recipient_name = data.get('recipient_name', '').strip()
    phone = data.get('phone', '').strip()
    address_line = data.get('address_line', '').strip()
    city = data.get('city', 'Chennai').strip()
    state = data.get('state', 'Tamil Nadu').strip()
    pincode = str(data.get('pincode', '')).strip()
    is_default = bool(data.get('is_default', False))

    if not recipient_name or not address_line or not pincode:
        return jsonify({'success': False, 'message': 'Recipient name, address line, and PIN code are required.'}), 400

    if not validate_phone(phone):
        return jsonify({'success': False, 'message': 'Please provide a valid 10-digit mobile number.'}), 400

    if not validate_pincode(pincode):
        return jsonify({'success': False, 'message': 'Please enter a valid 6-digit Indian PIN code.'}), 400

    # If first address or marked default, clear previous defaults
    has_existing = Address.query.filter_by(user_id=user_id).count() > 0
    if not has_existing or is_default:
        is_default = True
        Address.query.filter_by(user_id=user_id).update({'is_default': False})

    address = Address(
        user_id=user_id,
        recipient_name=recipient_name,
        phone=clean_phone(phone) or phone,
        address_line=address_line,
        city=city,
        state=state,
        pincode=pincode,
        is_default=is_default
    )
    db.session.add(address)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Address added successfully.',
        'address': address.to_dict()
    }), 201


@address_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_address(id):
    user_id = int(get_jwt_identity())
    address = Address.query.filter_by(id=id, user_id=user_id).first()
    if not address:
        return jsonify({'success': False, 'message': 'Address not found.'}), 404

    data = request.get_json() or {}
    if 'recipient_name' in data and data['recipient_name'].strip():
        address.recipient_name = data['recipient_name'].strip()
    if 'address_line' in data and data['address_line'].strip():
        address.address_line = data['address_line'].strip()
    if 'city' in data and data['city'].strip():
        address.city = data['city'].strip()
    if 'state' in data and data['state'].strip():
        address.state = data['state'].strip()

    if 'phone' in data:
        p = str(data['phone']).strip()
        if not validate_phone(p):
            return jsonify({'success': False, 'message': 'Invalid phone number format.'}), 400
        address.phone = clean_phone(p) or p

    if 'pincode' in data:
        pin = str(data['pincode']).strip()
        if not validate_pincode(pin):
            return jsonify({'success': False, 'message': 'Invalid 6-digit PIN code.'}), 400
        address.pincode = pin

    if 'is_default' in data and data['is_default']:
        Address.query.filter_by(user_id=user_id).update({'is_default': False})
        address.is_default = True

    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Address updated successfully.',
        'address': address.to_dict()
    }), 200


@address_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_address(id):
    user_id = int(get_jwt_identity())
    address = Address.query.filter_by(id=id, user_id=user_id).first()
    if not address:
        return jsonify({'success': False, 'message': 'Address not found.'}), 404

    db.session.delete(address)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Address deleted successfully.'
    }), 200


@address_bp.route('/<int:id>/set-default', methods=['PUT'])
@jwt_required()
def set_default_address(id):
    user_id = int(get_jwt_identity())
    address = Address.query.filter_by(id=id, user_id=user_id).first()
    if not address:
        return jsonify({'success': False, 'message': 'Address not found.'}), 404

    Address.query.filter_by(user_id=user_id).update({'is_default': False})
    address.is_default = True
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Default address set.',
        'address': address.to_dict()
    }), 200
