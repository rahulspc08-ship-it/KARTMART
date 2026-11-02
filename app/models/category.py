from app.extensions import db


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True, index=True)
    name = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(80), unique=True, nullable=False, index=True)
    icon = db.Column(db.String(20), default='📦')
    image_url = db.Column(db.String(500), nullable=True)
    description = db.Column(db.String(255), nullable=True)

    # Relationships
    subcategories = db.relationship('Category', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')
    products = db.relationship('Product', backref='category', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'parent_id': self.parent_id,
            'name': self.name,
            'slug': self.slug,
            'icon': self.icon,
            'image_url': self.image_url,
            'description': self.description,
            'product_count': self.products.count()
        }
