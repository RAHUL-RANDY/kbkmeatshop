from datetime import datetime
from app.extensions import db

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'), nullable=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False, index=True) # e.g. 'FMM-20261114-1001'
    
    subtotal = db.Column(db.Float, nullable=False)
    delivery_charge = db.Column(db.Float, default=0.0, nullable=False)
    discount_amount = db.Column(db.Float, default=0.0, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    
    order_status = db.Column(db.String(50), default='Pending', nullable=False, index=True)
    # Statuses: 'Pending', 'Confirmed', 'Processing', 'Out for Delivery', 'Delivered', 'Cancelled'
    
    payment_status = db.Column(db.String(50), default='Pending', nullable=False, index=True)
    # Statuses: 'Pending', 'Paid', 'Failed', 'Refunded'
    
    payment_method = db.Column(db.String(50), default='COD', nullable=False) # 'COD', 'Razorpay'
    coupon_code = db.Column(db.String(50), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    delivered_at = db.Column(db.DateTime, nullable=True, index=True)

    # Relationships
    items = db.relationship('OrderItem', backref='order', cascade='all, delete-orphan', lazy='joined')
    payment = db.relationship('Payment', backref='order', uselist=False, cascade='all, delete-orphan')
    address = db.relationship('Address', lazy='joined')

    def to_dict(self):
        return {
            'id': self.id,
            'order_number': self.order_number,
            'user_id': self.user_id,
            'customer_name': self.user.full_name if self.user else 'Customer',
            'customer_email': self.user.email if self.user else None,
            'customer_phone': self.address.phone if self.address else (self.user.phone if self.user else None),
            'customer_address': f"{self.address.address_line}, {self.address.city} - {self.address.pincode}" if self.address else None,
            'address': self.address.to_dict() if self.address else None,
            'items': [item.to_dict() for item in self.items],
            'items_count': sum(item.quantity for item in self.items),
            'subtotal': self.subtotal,
            'delivery_charge': self.delivery_charge,
            'discount_amount': self.discount_amount,
            'total_amount': self.total_amount,
            'order_status': self.order_status,
            'payment_status': self.payment_status,
            'payment_method': self.payment_method,
            'coupon_code': self.coupon_code,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'delivered_at': self.delivered_at.isoformat() if self.delivered_at else None
        }

    def __repr__(self):
        return f"<Order {self.order_number} (₹{self.total_amount}) - {self.order_status}>"


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    product_name = db.Column(db.String(150), nullable=False)
    selected_weight = db.Column(db.String(50), default='1 kg', nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    product_image = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'selected_weight': self.selected_weight,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'total_price': self.total_price,
            'product_image': self.product_image
        }
