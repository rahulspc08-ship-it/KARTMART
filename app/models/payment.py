from datetime import datetime
import uuid
from app.extensions import db


class PaymentRecord(db.Model):
    __tablename__ = 'payment_records'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    transaction_id = db.Column(db.String(100), unique=True, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(30), default='Success', nullable=False)
    is_simulated = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    order = db.relationship('Order', backref=db.backref('payment_record', uselist=False))

    @staticmethod
    def generate_transaction_id():
        return f"SIM-PAY-{uuid.uuid4().hex[:12].upper()}"
