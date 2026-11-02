from datetime import datetime
from app.extensions import db


class Coupon(db.Model):
    __tablename__ = 'coupons'

    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=True, index=True)
    code = db.Column(db.String(30), unique=True, nullable=False, index=True)
    discount_type = db.Column(db.String(20), default='percentage', nullable=False)  # 'percentage' or 'flat'
    discount_percent = db.Column(db.Integer, default=10, nullable=False)
    max_discount = db.Column(db.Float, default=1000.0, nullable=True)
    min_order_amount = db.Column(db.Float, default=0.0, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    times_used = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def is_expired(self):
        if not self.is_active:
            return True
        now = datetime.utcnow()
        if self.start_date and now < self.start_date:
            return True
        if self.end_date and now > self.end_date:
            return True
        return False

    def calculate_discount(self, order_subtotal):
        if self.is_expired or order_subtotal < self.min_order_amount:
            return 0.0

        if self.discount_type == 'flat':
            discount = float(self.max_discount or 0.0)
            return round(min(discount, order_subtotal), 2)

        raw_discount = (self.discount_percent / 100.0) * order_subtotal
        if self.max_discount and raw_discount > self.max_discount:
            return round(self.max_discount, 2)
        return round(raw_discount, 2)

    def to_dict(self):
        return {
            'code': self.code,
            'discount_type': self.discount_type,
            'discount_percent': self.discount_percent,
            'max_discount': self.max_discount,
            'min_order_amount': self.min_order_amount,
            'description': self.description,
            'is_expired': self.is_expired,
            'end_date': self.end_date.strftime('%d %b %Y') if self.end_date else None
        }
