from datetime import datetime
import random
from app.extensions import db


class SupportTicket(db.Model):
    __tablename__ = 'support_tickets'

    id = db.Column(db.Integer, primary_key=True)
    ticket_ref = db.Column(db.String(50), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    customer_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # 'Delivery', 'Refund & Cancellation', 'Product Issue', 'Payment', 'Other'
    order_ref = db.Column(db.String(50), nullable=True)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(30), default='Open', nullable=False)  # 'Open', 'In Progress', 'Resolved'
    admin_response = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', backref=db.backref('support_tickets', lazy='dynamic'))

    @staticmethod
    def generate_ticket_ref():
        timestamp = datetime.utcnow().strftime('%Y%m')
        rand = random.randint(1000, 9999)
        return f"TICK-{timestamp}-{rand}"

    def to_dict(self):
        return {
            'id': self.id,
            'ticket_ref': self.ticket_ref,
            'customer_name': self.customer_name,
            'email': self.email,
            'category': self.category,
            'order_ref': self.order_ref,
            'subject': self.subject,
            'message': self.message,
            'status': self.status,
            'admin_response': self.admin_response,
            'created_at': self.created_at.strftime('%d %b %Y, %I:%M %p')
        }
