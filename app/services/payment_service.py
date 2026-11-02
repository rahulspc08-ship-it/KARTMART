from app.extensions import db
from app.models import PaymentRecord


class PaymentService:

    @staticmethod
    def process_payment(order, payment_method):
        """
        Simulate an e-commerce payment transaction (UPI, Credit/Debit Card, or Cash on Delivery).
        Does not charge real money or connect to external gateways.
        """
        tx_id = PaymentRecord.generate_transaction_id()
        
        if payment_method == 'Cash on Delivery':
            order.payment_status = 'Pending on Delivery'
            order.order_status = 'Placed'
            record_status = 'Pending'
        else:
            order.payment_status = 'Paid (Simulated)'
            order.order_status = 'Confirmed'
            record_status = 'Success'

        record = PaymentRecord(
            order_id=order.id,
            transaction_id=tx_id,
            payment_method=payment_method,
            amount=order.total_amount,
            status=record_status,
            is_simulated=True
        )
        
        db.session.add(record)
        db.session.commit()
        
        return {
            'success': True,
            'transaction_id': tx_id,
            'method': payment_method,
            'amount': order.total_amount,
            'status': record_status
        }
