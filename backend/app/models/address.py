from datetime import datetime
from app.extensions import db

class Address(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    recipient_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address_line = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), default='Chennai', nullable=False)
    state = db.Column(db.String(100), default='Tamil Nadu', nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    is_default = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'recipient_name': self.recipient_name,
            'phone': self.phone,
            'address_line': self.address_line,
            'city': self.city,
            'state': self.state,
            'pincode': self.pincode,
            'is_default': self.is_default,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f"<Address {self.recipient_name}, {self.city} - {self.pincode}>"
