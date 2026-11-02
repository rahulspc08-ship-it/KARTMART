from datetime import datetime
from app.extensions import db


class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    session_id = db.Column(db.String(100), nullable=True, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    product = db.relationship('Product')

    @property
    def subtotal(self):
        if self.product:
            return round(self.product.price * self.quantity, 2)
        return 0.0

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else '',
            'product_emoji': self.product.emoji if self.product else '📦',
            'product_image': self.product.image_url if (self.product and self.product.image_url) else '/static/img/products/fallback.jpg',
            'product_price': self.product.price if self.product else 0.0,
            'quantity': self.quantity,
            'subtotal': self.subtotal,
            'stock': self.product.stock if self.product else 0
        }
