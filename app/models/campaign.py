from datetime import datetime
from app.extensions import db


class Campaign(db.Model):
    __tablename__ = 'campaigns'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    badge = db.Column(db.String(50), default='FESTIVE SALE')
    headline = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    banner_image = db.Column(db.String(500), nullable=True)
    discount_text = db.Column(db.String(100), nullable=True)  # e.g. "Flat 50% OFF"
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    coupons = db.relationship('Coupon', backref='campaign', lazy='dynamic')

    @property
    def is_currently_live(self):
        now = datetime.utcnow()
        return self.is_active and (self.start_date <= now <= self.end_date)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'badge': self.badge,
            'headline': self.headline,
            'description': self.description,
            'banner_image': self.banner_image,
            'discount_text': self.discount_text,
            'start_date': self.start_date.strftime('%Y-%m-%d %H:%M'),
            'end_date': self.end_date.strftime('%Y-%m-%d %H:%M'),
            'is_active': self.is_active,
            'is_currently_live': self.is_currently_live
        }
