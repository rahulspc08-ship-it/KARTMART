from datetime import datetime
from app.extensions import db


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    original_price = db.Column(db.Float, nullable=True)
    stock = db.Column(db.Integer, default=15, nullable=False)
    rating = db.Column(db.Float, default=4.5)
    reviews_count = db.Column(db.Integer, default=12)
    badge = db.Column(db.String(50), nullable=True)
    emoji = db.Column(db.String(20), default='📦')
    image_url = db.Column(db.String(500), nullable=True)
    additional_images = db.Column(db.Text, nullable=True)  # JSON or comma-separated list
    brand = db.Column(db.String(100), nullable=True)
    is_diwali_deal = db.Column(db.Boolean, default=False, nullable=False)
    is_featured = db.Column(db.Boolean, default=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    reviews = db.relationship('Review', backref='product', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def discount_percent(self):
        if self.original_price and self.original_price > self.price:
            return int(round(((self.original_price - self.price) / self.original_price) * 100))
        return 0

    @property
    def is_in_stock(self):
        return self.stock > 0

    def to_dict(self):
        return {
            'id': self.id,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else '',
            'name': self.name,
            'brand': self.brand,
            'description': self.description,
            'price': self.price,
            'original_price': self.original_price,
            'discount_percent': self.discount_percent,
            'stock': self.stock,
            'is_in_stock': self.is_in_stock,
            'is_diwali_deal': self.is_diwali_deal,
            'is_featured': self.is_featured,
            'rating': self.rating,
            'reviews_count': self.reviews_count,
            'badge': self.badge,
            'emoji': self.emoji,
            'image_url': self.image_url
        }
