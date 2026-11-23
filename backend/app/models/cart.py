from datetime import datetime
from app.extensions import db

class Cart(db.Model):
    __tablename__ = 'carts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    items = db.relationship('CartItem', backref='cart', cascade='all, delete-orphan', lazy='joined')

    def calculate_subtotal(self):
        return round(sum(item.total_price for item in self.items), 2)

    def to_dict(self):
        items_list = [item.to_dict() for item in self.items]
        subtotal = self.calculate_subtotal()
        free_delivery_threshold = 499.0
        delivery_charge = 0.0 if subtotal >= free_delivery_threshold or len(items_list) == 0 else 49.0
        total_amount = round(subtotal + delivery_charge, 2)

        return {
            'id': self.id,
            'user_id': self.user_id,
            'items': items_list,
            'items_count': sum(item.quantity for item in self.items),
            'subtotal': subtotal,
            'delivery_charge': delivery_charge,
            'free_delivery_threshold': free_delivery_threshold,
            'remaining_for_free_delivery': max(0.0, round(free_delivery_threshold - subtotal, 2)),
            'total_amount': total_amount,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, index=True)
    selected_weight = db.Column(db.String(50), default='1 kg', nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationship
    product = db.relationship('Product', lazy='joined')

    @property
    def total_price(self):
        return round(self.unit_price * self.quantity, 2)

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_code': self.product.product_code if self.product else None,
            'name': self.product.product_name if self.product else 'Unavailable Product',
            'image': self.product.image if self.product else None,
            'unit': self.product.unit if self.product else 'kg',
            'selected_weight': self.selected_weight,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'total_price': self.total_price,
            'is_in_stock': (self.product.stock_quantity >= self.quantity) if self.product else False
        }
