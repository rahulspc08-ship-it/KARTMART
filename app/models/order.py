from datetime import datetime
import random
from app.extensions import db


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_ref = db.Column(db.String(50), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    customer_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    shipping_address = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(80), nullable=False)
    pincode = db.Column(db.String(20), nullable=False)
    
    subtotal = db.Column(db.Float, nullable=False)
    discount_amount = db.Column(db.Float, default=0.0)
    coupon_code = db.Column(db.String(30), nullable=True)
    delivery_fee = db.Column(db.Float, default=0.0)
    total_amount = db.Column(db.Float, nullable=False)
    
    payment_method = db.Column(db.String(50), default='Cash on Delivery', nullable=False)
    payment_status = db.Column(db.String(50), default='Pending on Delivery', nullable=False)
    order_status = db.Column(db.String(50), default='Placed', nullable=False)
    
    # Cancellation & Refund tracking
    cancellation_reason = db.Column(db.String(150), nullable=True)
    cancellation_comments = db.Column(db.Text, nullable=True)
    cancelled_at = db.Column(db.DateTime, nullable=True)
    refund_status = db.Column(db.String(50), default='Not Applicable', nullable=False)  # 'Not Applicable', 'Pending', 'Processed to Source', 'Credited to Wallet'
    refund_amount = db.Column(db.Float, default=0.0, nullable=False)
    refund_ref = db.Column(db.String(50), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy='joined', cascade='all, delete-orphan')

    @staticmethod
    def generate_order_ref():
        timestamp = datetime.utcnow().strftime('%Y%m%d')
        rand_num = random.randint(1000, 9999)
        return f"KART-{timestamp}-{rand_num}"

    def can_be_cancelled(self):
        return self.order_status in ['Placed', 'Confirmed']

    def to_dict(self):
        return {
            'id': self.id,
            'order_ref': self.order_ref,
            'customer_name': self.customer_name,
            'email': self.email,
            'phone': self.phone,
            'shipping_address': self.shipping_address,
            'city': self.city,
            'pincode': self.pincode,
            'subtotal': self.subtotal,
            'discount_amount': self.discount_amount,
            'coupon_code': self.coupon_code,
            'total_amount': self.total_amount,
            'payment_method': self.payment_method,
            'payment_status': self.payment_status,
            'order_status': self.order_status,
            'cancellation_reason': self.cancellation_reason,
            'cancellation_comments': self.cancellation_comments,
            'cancelled_at': self.cancelled_at.strftime('%d %b %Y, %I:%M %p') if self.cancelled_at else None,
            'refund_status': self.refund_status,
            'refund_amount': self.refund_amount,
            'refund_ref': self.refund_ref,
            'created_at': self.created_at.strftime('%d %b %Y, %I:%M %p'),
            'item_count': sum(item.quantity for item in self.items),
            'items': [item.to_dict() for item in self.items]
        }


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    product_name = db.Column(db.String(200), nullable=False)
    product_emoji = db.Column(db.String(20), default='📦')
    product_image = db.Column(db.String(500), nullable=True)
    product_variant = db.Column(db.String(100), nullable=True)
    unit_price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    line_total = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'product_id': self.product_id,
            'product_name': self.product_name,
            'product_emoji': self.product_emoji,
            'product_image': self.product_image,
            'product_variant': self.product_variant,
            'unit_price': self.unit_price,
            'quantity': self.quantity,
            'line_total': self.line_total
        }
