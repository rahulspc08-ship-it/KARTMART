from app.extensions import db


class ProductVariant(db.Model):
    __tablename__ = 'product_variants'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, index=True)
    variant_type = db.Column(db.String(50), nullable=False)  # 'Color', 'Size', 'Storage', 'Style'
    variant_value = db.Column(db.String(100), nullable=False)  # 'Midnight Black', 'XL', '256GB'
    price_adjustment = db.Column(db.Float, default=0.0, nullable=False)
    stock = db.Column(db.Integer, default=10, nullable=False)
    sku = db.Column(db.String(50), nullable=True)

    # Relationships
    product = db.relationship('Product', backref=db.backref('variants', lazy='dynamic', cascade='all, delete-orphan'))

    def to_dict(self):
        return {
            'id': self.id,
            'variant_type': self.variant_type,
            'variant_value': self.variant_value,
            'price_adjustment': self.price_adjustment,
            'stock': self.stock,
            'sku': self.sku
        }
