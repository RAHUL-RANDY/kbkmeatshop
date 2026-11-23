from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.user import User
from app.models.order import Order
from app.services.order_service import OrderService
from app.services.notification_service import NotificationService

order_bp = Blueprint('orders', __name__, url_prefix='/api/orders')

@order_bp.route('', methods=['POST'])
@jwt_required(optional=True)
def place_order():
    raw_user_id = get_jwt_identity()
    data = request.get_json() or {}

    if raw_user_id:
        user = db.session.get(User, int(raw_user_id))
    else:
        # Guest Checkout: Find or create Guest Customer
        raw_email = (data.get('email') or data.get('customer_email') or '').strip().lower()
        guest_email = raw_email if (raw_email and '@' in raw_email) else f"customer_{data.get('phone', '9842729718')}@kbkmeatshop.com"
        user = User.query.filter_by(email=guest_email).first()
        if not user:
            user = User(
                full_name=data.get('recipient_name', 'Guest Customer').strip(),
                email=guest_email,
                phone=data.get('phone', '9842729718'),
                role='customer',
                is_active=True
            )
            user.set_password('Guest@123456')
            db.session.add(user)
            db.session.flush()
        else:
            if data.get('recipient_name'):
                user.full_name = data.get('recipient_name').strip()
            if data.get('phone'):
                user.phone = data.get('phone').strip()

    if not user:
        return jsonify({'success': False, 'message': 'User could not be initialized.'}), 404

    # Ensure user has a cart
    from app.models.cart import Cart, CartItem
    from app.models.product import Product
    from app.models.address import Address

    cart = Cart.query.filter_by(user_id=user.id).first()
    if not cart:
        cart = Cart(user_id=user.id)
        db.session.add(cart)
        db.session.flush()

    # If guest passed items from frontend cart, populate cart
    items_data = data.get('items', [])
    if items_data:
        for existing in list(cart.items):
            db.session.delete(existing)
        db.session.flush()

        for itm in items_data:
            prod_id = itm.get('id') or itm.get('product_id')
            qty = itm.get('quantity', 1)
            weight = itm.get('selectedWeight') or itm.get('selected_weight', '1 kg')
            prod = None
            if isinstance(prod_id, int) or (isinstance(prod_id, str) and prod_id.isdigit()):
                prod = db.session.get(Product, int(prod_id))
            if not prod and prod_id:
                prod = Product.query.filter_by(product_code=str(prod_id)).first()
            if prod:
                unit_price = prod.calculate_price_for_weight(weight)
                cart_item = CartItem(
                    cart_id=cart.id,
                    product_id=prod.id,
                    selected_weight=weight,
                    quantity=qty,
                    unit_price=unit_price
                )
                db.session.add(cart_item)
        db.session.flush()
        db.session.refresh(cart)

    # Address handling
    address_id = data.get('address_id')
    if not address_id and data.get('address_line'):
        new_addr = Address(
            user_id=user.id,
            recipient_name=data.get('recipient_name', user.full_name),
            phone=data.get('phone', user.phone or '9842729718'),
            address_line=data.get('address_line'),
            city=data.get('city', 'Chennai'),
            state=data.get('state', 'Tamil Nadu'),
            pincode=data.get('pincode', '600040'),
            is_default=True
        )
        db.session.add(new_addr)
        db.session.flush()
        address_id = new_addr.id
    elif not address_id:
        addr = Address.query.filter_by(user_id=user.id).first()
        if addr:
            address_id = addr.id
        else:
            new_addr = Address(
                user_id=user.id,
                recipient_name=user.full_name,
                phone=user.phone or '9842729718',
                address_line='Fresh Meat Weekend Delivery',
                city='Chennai',
                state='Tamil Nadu',
                pincode='600040',
                is_default=True
            )
            db.session.add(new_addr)
            db.session.flush()
            address_id = new_addr.id

    payment_method = data.get('payment_method', 'COD').strip() # 'COD' or 'Razorpay'
    coupon_code = data.get('coupon_code')
    delivery_day = data.get('delivery_day') or data.get('delivery_slot') or 'Saturday Morning (6 AM - 10 AM)'
    notes = data.get('notes') or f"Weekend Delivery: {delivery_day}"

    try:
        order = OrderService.create_order_from_cart(
            user=user,
            address_id=address_id,
            payment_method=payment_method,
            coupon_code=coupon_code,
            notes=notes
        )
        notification = NotificationService.send_order_notifications(order)
        order_dict = order.to_dict()
        order_dict['notification'] = notification

        return jsonify({
            'success': True,
            'message': 'Order placed successfully. WhatsApp & SMS message dispatched.',
            'order': order_dict
        }), 201
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': f'Failed to place order: {str(e)}'}), 500


@order_bp.route('', methods=['GET'])
@jwt_required()
def get_orders():
    user_id = int(get_jwt_identity())
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.id.desc()).all()
    return jsonify({
        'success': True,
        'count': len(orders),
        'orders': [o.to_dict() for o in orders]
    }), 200


@order_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_order_by_id(id):
    user_id = int(get_jwt_identity())
    order = Order.query.filter_by(id=id, user_id=user_id).first()
    if not order:
        return jsonify({'success': False, 'message': 'Order not found.'}), 404

    return jsonify({
        'success': True,
        'order': order.to_dict()
    }), 200


@order_bp.route('/<int:id>/cancel', methods=['PUT'])
@jwt_required()
def cancel_order(id):
    user_id = int(get_jwt_identity())
    order = Order.query.filter_by(id=id, user_id=user_id).first()
    if not order:
        return jsonify({'success': False, 'message': 'Order not found.'}), 404

    try:
        updated_order = OrderService.cancel_order(order, user_id=user_id)
        return jsonify({
            'success': True,
            'message': 'Order has been cancelled successfully.',
            'order': updated_order.to_dict()
        }), 200
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
