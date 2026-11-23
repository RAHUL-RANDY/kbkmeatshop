from datetime import datetime
from app.extensions import db

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), unique=True, nullable=False, index=True)
    payment_reference = db.Column(db.String(100), unique=True, nullable=False, index=True)
    payment_method = db.Column(db.String(50), default='COD', nullable=False) # 'COD', 'Razorpay'
    amount = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(50), default='Pending', nullable=False, index=True) # 'Pending', 'Success', 'Failed'
    
    razorpay_order_id = db.Column(db.String(100), nullable=True)
    razorpay_payment_id = db.Column(db.String(100), nullable=True)
    razorpay_signature = db.Column(db.String(255), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'payment_reference': self.payment_reference,
            'payment_method': self.payment_method,
            'amount': self.amount,
            'payment_status': self.payment_status,
            'razorpay_order_id': self.razorpay_order_id,
            'razorpay_payment_id': self.razorpay_payment_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f"<Payment {self.payment_reference} ({self.payment_status}) - ₹{self.amount}>"
