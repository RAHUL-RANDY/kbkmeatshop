import os
from datetime import datetime
from flask import Blueprint, request, jsonify
from sqlalchemy import func
from app.extensions import db
from app.models.user import User
from app.models.product import Product
from app.models.category import Category
from app.models.order import Order
from app.services.cleanup_service import CleanupService
from app.utils.validators import admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route('/dashboard', methods=['GET'])
@admin_required()
def get_dashboard():
    total_customers = User.query.filter_by(role='customer').count()
    total_products = Product.query.count()
    total_orders = Order.query.count()
    
    # Total sales from delivered or paid orders
    total_sales = db.session.query(func.coalesce(func.sum(Order.total_amount), 0.0)).filter(
        (Order.payment_status == 'Paid') | (Order.order_status.in_(['Confirmed', 'Delivered']))
    ).scalar()

    pending_orders = Order.query.filter(Order.order_status.in_(['Pending', 'Processing'])).count()
    completed_orders = Order.query.filter_by(order_status='Delivered').count()

    recent_orders = Order.query.order_by(Order.id.desc()).limit(5).all()

    return jsonify({
        'success': True,
        'stats': {
            'total_customers': total_customers,
            'total_products': total_products,
            'total_orders': total_orders,
            'total_sales': round(float(total_sales), 2),
            'pending_orders': pending_orders,
            'completed_orders': completed_orders
        },
        'recent_orders': [o.to_dict() for o in recent_orders]
    }), 200


@admin_bp.route('/orders', methods=['GET'])
@admin_required()
def get_admin_orders():
    status = request.args.get('status')
    query = Order.query

    if status and status != 'all':
        query = query.filter_by(order_status=status)

    orders = query.order_by(Order.id.desc()).all()
    return jsonify({
        'success': True,
        'count': len(orders),
        'orders': [o.to_dict() for o in orders]
    }), 200


@admin_bp.route('/orders/<int:id>/status', methods=['PUT'])
@admin_required()
def update_order_status(id):
    order = Order.query.get(id)
    if not order:
        return jsonify({'success': False, 'message': 'Order not found.'}), 404

    data = request.get_json() or {}
    new_order_status = data.get('order_status')
    new_payment_status = data.get('payment_status')

    valid_order_statuses = ['Pending', 'Confirmed', 'Processing', 'Out for Delivery', 'Delivered', 'Cancelled']
    valid_payment_statuses = ['Pending', 'Paid', 'Failed', 'Refunded']

    if new_order_status:
        if new_order_status not in valid_order_statuses:
            return jsonify({'success': False, 'message': f'Invalid order status. Allowed: {valid_order_statuses}'}), 400
        order.order_status = new_order_status
        if new_order_status == 'Delivered':
            if not order.delivered_at:
                order.delivered_at = datetime.utcnow()
        else:
            order.delivered_at = None

    if new_payment_status:
        if new_payment_status not in valid_payment_statuses:
            return jsonify({'success': False, 'message': f'Invalid payment status. Allowed: {valid_payment_statuses}'}), 400
        order.payment_status = new_payment_status
        if order.payment:
            order.payment.payment_status = 'Success' if new_payment_status == 'Paid' else new_payment_status

    db.session.commit()

    return jsonify({
        'success': True,
        'message': f'Order {order.order_number} status updated.',
        'order': order.to_dict()
    }), 200


@admin_bp.route('/products', methods=['POST'])
@admin_required()
def add_product():
    data = request.get_json() or {}

    product_name = data.get('name') or data.get('product_name')
    category_id = data.get('category_id')
    price = data.get('price')

    if not product_name or not category_id or price is None:
        return jsonify({'success': False, 'message': 'Product name, category_id, and price are required.'}), 400

    # Auto code if not provided
    product_code = data.get('product_code') or product_name.strip().lower().replace(' ', '-')

    existing = Product.query.filter_by(product_code=product_code).first()
    if existing:
        return jsonify({'success': False, 'message': f"Product code '{product_code}' already exists."}), 409

    product = Product(
        product_code=product_code,
        product_name=product_name.strip(),
        description=data.get('description', ''),
        category_id=int(category_id),
        price=float(price),
        original_price=float(data.get('original_price')) if data.get('original_price') else None,
        unit=data.get('unit', 'kg'),
        weight_options=data.get('weight_options', ['500 g', '1 kg', '2 kg']),
        default_weight=data.get('default_weight', '1 kg'),
        image=data.get('image', '/images/prod-country-chicken.jpg'),
        stock_quantity=int(data.get('stock_quantity', 100)),
        is_available=bool(data.get('is_available', True)),
        is_bestseller=bool(data.get('is_bestseller', False)),
        pieces=data.get('pieces', 'Hand Cut'),
        serves=data.get('serves', '3-4 Persons')
    )
    db.session.add(product)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Product added successfully.',
        'product': product.to_dict()
    }), 201


@admin_bp.route('/products/<int:id>', methods=['PUT'])
@admin_required()
def update_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'success': False, 'message': 'Product not found.'}), 404

    data = request.get_json() or {}

    if 'name' in data:
        product.product_name = data['name'].strip()
    if 'product_name' in data:
        product.product_name = data['product_name'].strip()
    if 'description' in data:
        product.description = data['description']
    if 'price' in data:
        product.price = float(data['price'])
    if 'original_price' in data:
        product.original_price = float(data['original_price']) if data['original_price'] else None
    if 'unit' in data:
        product.unit = data['unit']
    if 'stock_quantity' in data:
        product.stock_quantity = int(data['stock_quantity'])
    if 'is_available' in data:
        product.is_available = bool(data['is_available'])
    if 'is_bestseller' in data:
        product.is_bestseller = bool(data['is_bestseller'])
    if 'image' in data:
        product.image = data['image']
    if 'weight_options' in data:
        product.weight_options = data['weight_options']
    if 'default_weight' in data:
        product.default_weight = data['default_weight']
    if 'category_id' in data:
        product.category_id = int(data['category_id'])

    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Product updated successfully.',
        'product': product.to_dict()
    }), 200


@admin_bp.route('/products/<int:id>', methods=['DELETE'])
@admin_required()
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'success': False, 'message': 'Product not found.'}), 404

    from app.models.order import OrderItem
    from app.models.cart import CartItem

    # Remove from active cart items
    CartItem.query.filter_by(product_id=id).delete()

    has_orders = OrderItem.query.filter_by(product_id=id).first()
    if has_orders:
        product.is_available = False
        db.session.commit()
        return jsonify({
            'success': True,
            'message': f"Product '{product.product_name}' has previous orders, deactivated from marketplace."
        }), 200
    else:
        db.session.delete(product)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': f"Product '{product.product_name}' permanently removed."
        }), 200


@admin_bp.route('/customers', methods=['GET'])
@admin_required()
def get_customers():
    customers = User.query.filter_by(role='customer').order_by(User.id.desc()).all()
    result = []
    for c in customers:
        orders_count = c.orders.count()
        total_spent = db.session.query(func.coalesce(func.sum(Order.total_amount), 0.0)).filter_by(user_id=c.id).scalar()
        item = c.to_dict()
        item['orders_count'] = orders_count
        item['total_spent'] = round(float(total_spent), 2)
        result.append(item)

    return jsonify({
        'success': True,
        'count': len(result),
        'customers': result
    }), 200


@admin_bp.route('/customers/<int:id>/status', methods=['PUT'])
@admin_required()
def toggle_customer_status(id):
    customer = User.query.get(id)
    if not customer or customer.role == 'admin':
        return jsonify({'success': False, 'message': 'Customer not found or invalid target.'}), 404

    data = request.get_json() or {}
    is_active = data.get('is_active', not customer.is_active)
    customer.is_active = bool(is_active)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': f"Customer account has been {'activated' if customer.is_active else 'deactivated'}.",
        'customer': customer.to_dict()
    }), 200


def _persist_env_var(key, value):
    """Persists a key=value pair directly into backend/.env file"""
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
    try:
        lines = []
        if os.path.exists(env_path):
            with open(env_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        found = False
        new_lines = []
        for line in lines:
            if line.strip().startswith(f"{key}="):
                new_lines.append(f"{key}={value}\n")
                found = True
            else:
                new_lines.append(line)
        if not found:
            new_lines.append(f"\n{key}={value}\n")
        with open(env_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
    except Exception as e:
        print(f"[ENV Update Error]: {e}")


@admin_bp.route('/settings', methods=['GET'])
@admin_required()
def get_settings():
    admin_user = User.query.filter_by(role='admin').first()
    store_phone = (admin_user.phone if admin_user and admin_user.phone else None) or os.getenv('ADMIN_PHONE', '9842729718')
    store_email = os.getenv('ADMIN_EMAIL') or (admin_user.email if admin_user else 'kbkmeatshop@gmail.com')
    smtp_user = os.getenv('SMTP_USER', '')
    smtp_configured = bool(os.getenv('SMTP_USER') and os.getenv('SMTP_PASSWORD'))
    ultramsg_instance = os.getenv('ULTRAMSG_INSTANCE_ID', '')
    ultramsg_configured = bool(os.getenv('ULTRAMSG_INSTANCE_ID') and os.getenv('ULTRAMSG_TOKEN'))
    return jsonify({
        'success': True,
        'store_phone': store_phone,
        'store_email': store_email,
        'smtp_user': smtp_user,
        'smtp_configured': smtp_configured,
        'ultramsg_instance': ultramsg_instance,
        'ultramsg_configured': ultramsg_configured,
        'admin_name': admin_user.full_name if admin_user else 'Market Administrator',
        'admin_phone': admin_user.phone if admin_user else store_phone,
        'admin_email': store_email
    }), 200


@admin_bp.route('/settings', methods=['PUT'])
@admin_required()
def update_settings():
    data = request.get_json() or {}
    phone = data.get('store_phone') or data.get('admin_phone')
    email = data.get('store_email') or data.get('admin_email')
    smtp_user = data.get('smtp_user')
    smtp_password = data.get('smtp_password')
    ultramsg_instance = data.get('ultramsg_instance')
    ultramsg_token = data.get('ultramsg_token')
    
    admin_user = User.query.filter_by(role='admin').first()

    if phone:
        clean_phone = ''.join(c for c in str(phone) if c.isdigit())
        if clean_phone:
            os.environ['ADMIN_PHONE'] = clean_phone
            _persist_env_var('ADMIN_PHONE', clean_phone)
            if admin_user:
                admin_user.phone = clean_phone

    if email and '@' in str(email):
        clean_email = str(email).strip().lower()
        os.environ['ADMIN_EMAIL'] = clean_email
        _persist_env_var('ADMIN_EMAIL', clean_email)
        if admin_user:
            admin_user.email = clean_email

    if smtp_user is not None:
        clean_smtp_user = str(smtp_user).strip().lower()
        os.environ['SMTP_USER'] = clean_smtp_user
        _persist_env_var('SMTP_USER', clean_smtp_user)

    if smtp_password is not None:
        clean_smtp_pwd = str(smtp_password).strip()
        os.environ['SMTP_PASSWORD'] = clean_smtp_pwd
        _persist_env_var('SMTP_PASSWORD', clean_smtp_pwd)

    if ultramsg_instance is not None:
        clean_inst = str(ultramsg_instance).strip()
        os.environ['ULTRAMSG_INSTANCE_ID'] = clean_inst
        _persist_env_var('ULTRAMSG_INSTANCE_ID', clean_inst)

    if ultramsg_token is not None:
        clean_tok = str(ultramsg_token).strip()
        os.environ['ULTRAMSG_TOKEN'] = clean_tok
        _persist_env_var('ULTRAMSG_TOKEN', clean_tok)

    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Store owner alert settings updated successfully.',
        'store_phone': os.getenv('ADMIN_PHONE', '9842729718'),
        'store_email': os.getenv('ADMIN_EMAIL', 'kbkmeatshop@gmail.com'),
        'smtp_configured': bool(os.getenv('SMTP_USER') and os.getenv('SMTP_PASSWORD')),
        'ultramsg_configured': bool(os.getenv('ULTRAMSG_INSTANCE_ID') and os.getenv('ULTRAMSG_TOKEN'))
    }), 200


@admin_bp.route('/test-email', methods=['POST'])
@admin_required()
def test_email():
    data = request.get_json() or {}
    target_email = data.get('email') or os.getenv('ADMIN_EMAIL', 'admin@freshmeatmarket.com')
    
    from app.services.email_service import EmailService
    subject = "🧪 [TEST EMAIL] KBK MEAT SHOP Order Alert System"
    text_content = f"Hello Store Owner!\n\nThis is a verified test email from your KBK MEAT SHOP store.\nOrder notifications will be delivered to this email ({target_email}) automatically when customers book their meat cuts.\n\nHelpline: +91 98427 29718"
    html_content = f"""
    <div style="font-family: sans-serif; background-color: #170508; color: #fff; padding: 25px; border-radius: 16px; border: 1px solid #4a151b;">
        <h2 style="color: #fb7185; margin: 0 0 10px;">🥩 KBK MEAT SHOP - Email Alert Verified!</h2>
        <p style="color: #e5e7eb; font-size: 14px;">This test confirms that your order alert email is configured to receive automated order details directly at <strong>{target_email}</strong>.</p>
        <p style="color: #9ca3af; font-size: 12px; margin-top: 20px;">Store WhatsApp Helpline: +91 98427 29718</p>
    </div>
    """
    
    success = EmailService.send_email_sync(target_email, subject, text_content, html_content)
    return jsonify({
        'success': True,
        'message': f"Test email dispatched to {target_email} successfully.",
        'delivered': success
    }), 200


@admin_bp.route('/cleanup-expired-orders', methods=['POST'])
@admin_required()
def run_cleanup_expired_orders():
    data = request.get_json() or {}
    days = data.get('days', 2)
    result = CleanupService.cleanup_expired_delivered_orders(days=days)
    return jsonify(result), 200


@admin_bp.route('/retention-policy', methods=['GET'])
@admin_required()
def get_retention_policy():
    return jsonify({
        'success': True,
        'retention_policy_days': 2,
        'policy_description': 'Customer personal data and order records are permanently deleted 2 days after delivery.',
        'automated_scheduler': 'Active (Periodic Background Worker)'
    }), 200

