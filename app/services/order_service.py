from datetime import datetime
from app.extensions import db
from app.models import Order, OrderItem
from app.services.inventory_service import InventoryService
from app.services.coupon_service import CouponService
from app.services.payment_service import PaymentService
from app.services.notification_service import NotificationService


class OrderService:

    CANCELLATION_REASONS = [
        "Ordered by mistake",
        "Found a better price elsewhere",
        "Delivery is taking too long",
        "Product is no longer needed",
        "Selected the wrong product, size, or variant",
        "Payment-related issue",
        "Want to change the order",
        "Other reason"
    ]

    @classmethod
    def create_order_from_cart(cls, customer_data, cart_items, user_id=None, coupon_code=None):
        if not cart_items:
            return None, "Shopping cart is empty"

        # 1. Re-validate stock for every item
        for item in cart_items:
            available, msg = InventoryService.check_availability(item.product_id, item.quantity)
            if not available:
                return None, msg

        # 2. Trusted server-side calculation
        subtotal = sum(item.product.price * item.quantity for item in cart_items)
        discount_amount, coupon_obj, _ = CouponService.validate_and_apply(coupon_code, subtotal)
        delivery_fee = 0.0 if (subtotal > 499) else 40.0
        final_total = max(round(subtotal - discount_amount + delivery_fee, 2), 0.0)

        # 3. Create Order
        order_ref = Order.generate_order_ref()
        payment_method = customer_data.get('payment_method', 'Cash on Delivery')
        
        order = Order(
            order_ref=order_ref,
            user_id=user_id,
            customer_name=customer_data.get('customer_name', '').strip(),
            email=customer_data.get('email', '').strip(),
            phone=customer_data.get('phone', '').strip(),
            shipping_address=customer_data.get('shipping_address', '').strip(),
            city=customer_data.get('city', '').strip(),
            pincode=customer_data.get('pincode', '').strip(),
            subtotal=subtotal,
            discount_amount=discount_amount,
            coupon_code=coupon_obj.code if coupon_obj else None,
            delivery_fee=delivery_fee,
            total_amount=final_total,
            payment_method=payment_method,
            order_status='Placed'
        )

        db.session.add(order)
        db.session.flush()  # Generates order.id

        # 4. Create OrderItems & Deduct Stock
        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                product_name=item.product.name,
                product_emoji=item.product.emoji,
                product_image=item.product.image_url,
                unit_price=item.product.price,
                quantity=item.quantity,
                line_total=round(item.product.price * item.quantity, 2)
            )
            db.session.add(order_item)
            InventoryService.deduct_stock(item.product_id, item.quantity)

        # 5. Process Payment Simulation
        PaymentService.process_payment(order, payment_method)

        # 6. Notification
        NotificationService.notify(
            title="Order Placed Successfully",
            message=f"Order {order.order_ref} placed for ₹{order.total_amount}. Delivery expected in 2-3 business days.",
            user_id=user_id,
            category='order',
            icon='📦'
        )

        db.session.commit()
        return order, None

    @staticmethod
    def get_user_orders(user_id):
        return Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()

    @staticmethod
    def get_order_by_ref(order_ref):
        return Order.query.filter_by(order_ref=order_ref).first()

    @classmethod
    def cancel_order(cls, order_id, user_id=None, reason=None, comments=None, refund_method='source', is_admin=False):
        order = Order.query.get(order_id)
        if not order:
            return False, "Order not found", None

        # Permission check
        if order.user_id and order.user_id != user_id and not is_admin:
            return False, "Unauthorized to cancel this order", None

        # Status guard: strictly prevent cancellation after dispatch/delivery
        if not order.can_be_cancelled():
            return False, f"Order cannot be cancelled because it is already {order.order_status}.", order

        # Reason validation
        if not reason or reason not in cls.CANCELLATION_REASONS:
            return False, "Please select a valid cancellation reason.", order

        if reason == "Other reason" and (not comments or len(comments.strip()) < 5):
            return False, "Please provide a brief explanation for cancelling this order.", order

        # Restore inventory
        for item in order.items:
            if item.product_id:
                InventoryService.restore_stock(item.product_id, item.quantity)

        # Update order cancellation metadata
        order.order_status = 'Cancelled'
        order.cancellation_reason = reason
        order.cancellation_comments = comments.strip() if comments else None
        order.cancelled_at = datetime.utcnow()

        # Handle simulated refund calculation
        if order.payment_method == 'Cash on Delivery':
            order.refund_status = 'Not Applicable (COD)'
            order.refund_amount = 0.0
            order.refund_ref = None
        else:
            order.refund_amount = order.total_amount
            ref_id = f"REF-{datetime.utcnow().strftime('%Y%m%d')}-{order.order_ref.split('-')[-1]}"
            if refund_method == 'wallet':
                order.refund_status = 'Credited to KARTMART Wallet (Instant)'
                order.refund_ref = f"WAL-{ref_id}"
            else:
                order.refund_status = 'Processed to Original Source (Simulated 2-3 Business Days)'
                order.refund_ref = ref_id

        # Notification
        NotificationService.notify(
            title=f"Order {order.order_ref} Cancelled",
            message=f"Order has been cancelled. Refund status: {order.refund_status}.",
            user_id=order.user_id,
            category='order',
            icon='🚫'
        )

        db.session.commit()
        return True, "Your order has been cancelled successfully.", order

    @classmethod
    def update_status(cls, order_id, new_status):
        order = Order.query.get(order_id)
        if not order:
            return False, "Order not found"

        valid_statuses = ['Placed', 'Confirmed', 'Shipped', 'Out for Delivery', 'Delivered', 'Cancelled']
        if new_status not in valid_statuses:
            return False, f"Invalid status: {new_status}"

        # Cannot cancel shipped or delivered orders
        if new_status == 'Cancelled' and order.order_status in ['Shipped', 'Out for Delivery', 'Delivered']:
            return False, f"Cannot cancel order once it has been {order.order_status}"

        # If cancelled, restore inventory
        if new_status == 'Cancelled' and order.order_status != 'Cancelled':
            for item in order.items:
                if item.product_id:
                    InventoryService.restore_stock(item.product_id, item.quantity)

        order.order_status = new_status
        db.session.commit()
        return True, f"Order status updated to {new_status}"
