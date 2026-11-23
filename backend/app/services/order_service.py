import uuid
from datetime import datetime, timezone
from app.extensions import db
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.cart import Cart
from app.models.address import Address
from app.models.payment import Payment

class OrderService:

    @staticmethod
    def create_order_from_cart(user, address_id, payment_method='COD', coupon_code=None, notes=None):
        """
        Creates an order from the user's active cart within a database transaction.
        Verifies stock availability and calculates all prices on the server.
        """
        cart = Cart.query.filter_by(user_id=user.id).first()
        if not cart or not cart.items:
            raise ValueError("Your cart is empty. Please add items before placing an order.")

        # Address verification
        address = None
        if address_id:
            address = Address.query.filter_by(id=address_id, user_id=user.id).first()
            if not address:
                raise ValueError("Selected delivery address was not found.")

        # Validate stock & calculate subtotal on backend
        subtotal = 0.0
        order_items_data = []

        for item in cart.items:
            product = db.session.get(Product, item.product_id, with_for_update=True)
            if not product or not product.is_available:
                raise ValueError(f"Product '{item.product.product_name if item.product else 'Unknown'}' is currently unavailable.")
            
            if product.stock_quantity < item.quantity:
                raise ValueError(
                    f"Insufficient stock for '{product.product_name}'. Available: {product.stock_quantity}, requested: {item.quantity}."
                )

            # Calculate server-verified price based on weight
            unit_price = product.calculate_price_for_weight(item.selected_weight)
            item_total = round(unit_price * item.quantity, 2)
            subtotal += item_total

            # Deduct stock
            product.stock_quantity -= item.quantity

            order_items_data.append({
                'product_id': product.id,
                'product_name': product.product_name,
                'selected_weight': item.selected_weight,
                'quantity': item.quantity,
                'unit_price': unit_price,
                'total_price': item_total,
                'product_image': product.image
            })

        subtotal = round(subtotal, 2)

        # Calculate Delivery Fee (Free above 499)
        free_delivery_threshold = 499.0
        delivery_charge = 0.0 if subtotal >= free_delivery_threshold else 49.0

        # Apply Discount Coupons
        discount_amount = 0.0
        clean_coupon = coupon_code.strip().upper() if coupon_code else None
        if clean_coupon:
            if clean_coupon == 'FRESH20':
                discount_amount = round(subtotal * 0.20, 2)
            elif clean_coupon == 'PRIME30':
                discount_amount = round(subtotal * 0.30, 2)

        total_amount = max(0.0, round(subtotal - discount_amount + delivery_charge, 2))

        # Generate Unique Order Number
        today_str = datetime.now(timezone.utc).strftime('%Y%m%d')
        unique_suffix = uuid.uuid4().hex[:6].upper()
        order_number = f"FMM-{today_str}-{unique_suffix}"

        # Create Order
        order = Order(
            user_id=user.id,
            address_id=address.id if address else None,
            order_number=order_number,
            subtotal=subtotal,
            delivery_charge=delivery_charge,
            discount_amount=discount_amount,
            total_amount=total_amount,
            order_status='Confirmed' if payment_method == 'COD' else 'Pending',
            payment_status='Pending',
            payment_method=payment_method,
            coupon_code=clean_coupon,
            notes=notes
        )
        db.session.add(order)
        db.session.flush() # obtain order.id

        # Create Order Items
        for item_data in order_items_data:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item_data['product_id'],
                product_name=item_data['product_name'],
                selected_weight=item_data['selected_weight'],
                quantity=item_data['quantity'],
                unit_price=item_data['unit_price'],
                total_price=item_data['total_price'],
                product_image=item_data['product_image']
            )
            db.session.add(order_item)

        # Create Payment Record
        payment_ref = f"PAY-{uuid.uuid4().hex[:8].upper()}"
        payment = Payment(
            order_id=order.id,
            payment_reference=payment_ref,
            payment_method=payment_method,
            amount=total_amount,
            payment_status='Pending'
        )
        db.session.add(payment)

        # Clear User's Cart
        for item in list(cart.items):
            db.session.delete(item)

        db.session.commit()
        return order

    @staticmethod
    def cancel_order(order, user_id=None, is_admin=False):
        """
        Cancels an eligible order and restores product stock.
        """
        if not is_admin and order.user_id != user_id:
            raise PermissionError("You do not have permission to cancel this order.")

        if order.order_status in ['Delivered', 'Cancelled']:
            raise ValueError(f"Order cannot be cancelled because it is already '{order.order_status}'.")

        # Restore stock quantities
        for item in order.items:
            if item.product_id:
                product = db.session.get(Product, item.product_id)
                if product:
                    product.stock_quantity += item.quantity

        order.order_status = 'Cancelled'
        if order.payment_status == 'Pending':
            order.payment_status = 'Cancelled'
        elif order.payment_status == 'Paid':
            order.payment_status = 'Refunded'

        if order.payment:
            order.payment.payment_status = 'Failed' if order.payment.payment_status == 'Pending' else 'Refunded'

        db.session.commit()
        return order
