from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.cart import Cart, CartItem
from app.models.product import Product

cart_bp = Blueprint('cart', __name__, url_prefix='/api/cart')

def get_or_create_user_cart(user_id):
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.session.add(cart)
        db.session.commit()
    return cart

@cart_bp.route('', methods=['GET'])
@jwt_required()
def get_cart():
    user_id = int(get_jwt_identity())
    cart = get_or_create_user_cart(user_id)
    return jsonify({
        'success': True,
        'cart': cart.to_dict()
    }), 200


@cart_bp.route('/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    user_id = int(get_jwt_identity())
    cart = get_or_create_user_cart(user_id)
    data = request.get_json() or {}

    product_id = data.get('product_id')
    product_code = data.get('product_code')
    quantity = int(data.get('quantity', 1))
    selected_weight = data.get('selected_weight', '').strip()

    if quantity <= 0:
        return jsonify({'success': False, 'message': 'Quantity must be at least 1.'}), 400

    # Locate product
    product = None
    if product_id:
        product = Product.query.get(product_id)
    elif product_code:
        product = Product.query.filter_by(product_code=product_code).first()

    if not product or not product.is_available:
        return jsonify({'success': False, 'message': 'Product is currently unavailable.'}), 404

    # Determine weight choice
    if not selected_weight:
        selected_weight = product.default_weight or '1 kg'

    # Check available stock
    if product.stock_quantity < quantity:
        return jsonify({
            'success': False,
            'message': f'Cannot add {quantity} units. Only {product.stock_quantity} left in stock.'
        }), 400

    # Calculate verified unit price on backend
    unit_price = product.calculate_price_for_weight(selected_weight)

    # Check if this exact product + weight combination is already in cart
    existing_item = CartItem.query.filter_by(
        cart_id=cart.id,
        product_id=product.id,
        selected_weight=selected_weight
    ).first()

    if existing_item:
        new_qty = existing_item.quantity + quantity
        if product.stock_quantity < new_qty:
            return jsonify({
                'success': False,
                'message': f'Cannot exceed available stock of {product.stock_quantity}.'
            }), 400
        existing_item.quantity = new_qty
        existing_item.unit_price = unit_price
    else:
        new_item = CartItem(
            cart_id=cart.id,
            product_id=product.id,
            selected_weight=selected_weight,
            quantity=quantity,
            unit_price=unit_price
        )
        db.session.add(new_item)

    db.session.commit()

    return jsonify({
        'success': True,
        'message': f'Added {product.product_name} ({selected_weight}) to your cart.',
        'cart': cart.to_dict()
    }), 200


@cart_bp.route('/update/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_cart_item(item_id):
    user_id = int(get_jwt_identity())
    cart = get_or_create_user_cart(user_id)
    data = request.get_json() or {}
    new_quantity = int(data.get('quantity', 1))

    item = CartItem.query.filter_by(id=item_id, cart_id=cart.id).first()
    if not item:
        return jsonify({'success': False, 'message': 'Cart item not found.'}), 404

    if new_quantity <= 0:
        db.session.delete(item)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Item removed from cart.',
            'cart': cart.to_dict()
        }), 200

    # Stock validation
    if item.product and item.product.stock_quantity < new_quantity:
        return jsonify({
            'success': False,
            'message': f'Only {item.product.stock_quantity} units available in stock.'
        }), 400

    item.quantity = new_quantity
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Cart updated.',
        'cart': cart.to_dict()
    }), 200


@cart_bp.route('/remove/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_cart_item(item_id):
    user_id = int(get_jwt_identity())
    cart = get_or_create_user_cart(user_id)

    item = CartItem.query.filter_by(id=item_id, cart_id=cart.id).first()
    if not item:
        return jsonify({'success': False, 'message': 'Cart item not found.'}), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Item removed from cart.',
        'cart': cart.to_dict()
    }), 200


@cart_bp.route('/clear', methods=['DELETE'])
@jwt_required()
def clear_cart():
    user_id = int(get_jwt_identity())
    cart = get_or_create_user_cart(user_id)

    for item in list(cart.items):
        db.session.delete(item)

    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Cart cleared.',
        'cart': cart.to_dict()
    }), 200
