import json
from datetime import datetime
from app.extensions import db

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    product_code = db.Column(db.String(80), unique=True, nullable=False, index=True) # e.g. 'country-chicken'
    product_name = db.Column(db.String(150), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False, index=True)
    
    price = db.Column(db.Float, nullable=False) # base price
    original_price = db.Column(db.Float, nullable=True)
    unit = db.Column(db.String(50), default='kg', nullable=False) # 'kg', '30 Eggs', '500 g'
    
    # JSON-encoded array of weight choices, e.g. '["500 g", "1 kg", "2 kg"]'
    _weight_options = db.Column('weight_options', db.Text, default='["500 g", "1 kg", "2 kg"]')
    default_weight = db.Column(db.String(50), default='1 kg')
    
    image = db.Column(db.String(255), nullable=True)
    stock_quantity = db.Column(db.Integer, default=100, nullable=False)
    is_available = db.Column(db.Boolean, default=True, nullable=False, index=True)
    is_bestseller = db.Column(db.Boolean, default=False, nullable=False, index=True)
    
    rating = db.Column(db.Float, default=4.9)
    reviews_count = db.Column(db.Integer, default=150)
    pieces = db.Column(db.String(100), default='10-14 Pieces')
    serves = db.Column(db.String(100), default='3-4 Persons')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    @property
    def weight_options(self):
        try:
            return json.loads(self._weight_options) if self._weight_options else ['1 kg']
        except Exception:
            return ['1 kg']

    @weight_options.setter
    def weight_options(self, value):
        if isinstance(value, list):
            self._weight_options = json.dumps(value)
        elif isinstance(value, str):
            self._weight_options = value
        else:
            self._weight_options = '["1 kg"]'

    def calculate_price_for_weight(self, weight_str):
        """
        Calculate adjusted price on the backend based on weight/pack selection.
        Guarantees backend price calculation integrity.
        """
        if not weight_str:
            return self.price

        w = weight_str.strip().lower()
        base = float(self.price or 0.0)
        unit = (self.unit or '').strip().lower()
        default_w = (self.default_weight or '').strip().lower()

        # If base unit is 500 g (e.g. Salmon @ ₹650 for 500 g)
        if '500' in unit or '500 g' in default_w:
            if '250' in w and 'g' in w:
                return round(base * 0.5, 2)
            elif '500' in w and 'g' in w:
                return base
            elif '1' in w and 'kg' in w:
                return round(base * 2.0, 2)
            elif '2' in w and 'kg' in w:
                return round(base * 4.0, 2)

        # Eggs pack scaling (e.g. 30 eggs @ ₹160)
        if 'egg' in w or (self.category and self.category.slug == 'eggs'):
            if '6' in w:
                return round(base * (6.0 / 30.0), 2)
            elif '12' in w:
                return round(base * (12.0 / 30.0), 2)
            elif '30' in w or '1 pack' in w:
                return base

        # Standard per-kg meat items (Chicken, Mutton, Fish)
        if '250' in w and 'g' in w:
            return round(base * 0.25, 2)
        elif '500' in w and 'g' in w:
            return round(base * 0.5, 2)
        elif '1.5' in w and 'kg' in w:
            return round(base * 1.5, 2)
        elif '2' in w and 'kg' in w:
            return round(base * 2.0, 2)
        elif '1' in w and 'kg' in w:
            return base

        return base

    def to_dict(self):
        return {
            'id': self.id,
            'product_code': self.product_code,
            'name': self.product_name,
            'product_name': self.product_name,
            'description': self.description or '',
            'category_id': self.category_id,
            'category': self.category.slug if self.category else None,
            'category_name': self.category.category_name if self.category else None,
            'price': self.price,
            'original_price': self.original_price,
            'originalPrice': self.original_price,
            'unit': self.unit,
            'weight_options': self.weight_options,
            'weightOptions': self.weight_options,
            'default_weight': self.default_weight,
            'defaultWeight': self.default_weight,
            'image': self.image,
            'stock_quantity': self.stock_quantity,
            'is_available': self.is_available,
            'isAvailable': self.is_available,
            'is_bestseller': self.is_bestseller,
            'isBestseller': self.is_bestseller,
            'rating': self.rating,
            'reviews': self.reviews_count,
            'pieces': self.pieces or 'Hand Cut',
            'serves': self.serves or '3-4 Persons',
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f"<Product {self.product_name} (₹{self.price}/{self.unit})>"
