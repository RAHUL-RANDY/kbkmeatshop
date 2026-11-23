from datetime import datetime
from app.extensions import db

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False, index=True) # e.g. 'chicken', 'mutton', 'fish', 'eggs'
    subtitle = db.Column(db.String(150), nullable=True)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(255), nullable=True)
    item_count_label = db.Column(db.String(50), default='Available', nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    products = db.relationship('Product', backref='category', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'category_name': self.category_name,
            'slug': self.slug,
            'subtitle': self.subtitle,
            'description': self.description,
            'image': self.image,
            'item_count_label': self.item_count_label,
            'is_active': self.is_active,
            'products_count': self.products.filter_by(is_available=True).count(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f"<Category {self.category_name}>"
