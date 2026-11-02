from datetime import datetime
from app.extensions import db


class Address(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    recipient_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    street_address = db.Column(db.Text, nullable=False)
    landmark = db.Column(db.String(150), nullable=True)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False, default='Telangana')
    pincode = db.Column(db.String(20), nullable=False)
    address_type = db.Column(db.String(20), default='Home', nullable=False)  # 'Home', 'Work', 'Other'
    is_default = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', backref=db.backref('addresses', lazy='dynamic', cascade='all, delete-orphan'))

    def to_dict(self):
        return {
            'id': self.id,
            'recipient_name': self.recipient_name,
            'phone': self.phone,
            'street_address': self.street_address,
            'landmark': self.landmark,
            'city': self.city,
            'state': self.state,
            'pincode': self.pincode,
            'address_type': self.address_type,
            'is_default': self.is_default,
            'formatted': f"{self.street_address}, {self.city}, {self.state} - {self.pincode}"
        }
