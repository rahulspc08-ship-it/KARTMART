from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from app.extensions import db
from app.models import SupportTicket

support_bp = Blueprint('support', __name__)

FAQ_DATA = [
    {
        'category': 'Orders & Delivery',
        'icon': '📦',
        'questions': [
            {
                'q': 'How do I track my active order?',
                'a': 'You can track your order in real time by clicking on "Returns & Orders" in the navigation bar, or visiting your Account Dashboard and selecting the specific order reference number. A visual progress timeline will show you current transit milestones.'
            },
            {
                'q': 'What are the delivery charges and timelines?',
                'a': 'Orders above ₹499 qualify for FREE standard delivery across India. Standard orders are delivered within 2-3 business days. For orders under ₹499, a nominal delivery fee of ₹40 applies.'
            },
            {
                'q': 'Can I change my delivery address after placing an order?',
                'a': 'Delivery addresses can be updated before shipment by contacting support. If the order has already been dispatched, our courier partner will contact you via mobile on delivery day for location adjustments.'
            }
        ]
    },
    {
        'category': 'Cancellations & Refunds',
        'icon': '🛑',
        'questions': [
            {
                'q': 'How do I cancel my order?',
                'a': 'Open your order in "Returns & Orders" or "Track Order", click "Cancel Order", select the reason for cancellation, and confirm. Orders in "Placed" or "Confirmed" status can be cancelled immediately.'
            },
            {
                'q': 'Why can’t I cancel my order once it is shipped?',
                'a': 'Once an order has been shipped or out for delivery, it is already with the logistics courier in-transit and cannot be intercepted. You may refuse delivery at your doorstep, or request a return upon delivery.'
            },
            {
                'q': 'How long does a refund take?',
                'a': 'For simulated UPI and Card payments, refunds processed to your original payment method reflect in 2-3 business days. If you select KARTMART Wallet Balance, the refund credit is applied instantly.'
            }
        ]
    },
    {
        'category': 'Festival Offers & Coupons',
        'icon': '🪔',
        'questions': [
            {
                'q': 'How do I use festive promo codes like DIWALI50?',
                'a': 'On the checkout page, locate the "Apply Promo Code" card on the right order summary sidebar. Enter your code (or tap any available coupon chip) and click "Apply". Eligible discounts will be deducted immediately from your total amount.'
            },
            {
                'q': 'What happens if a coupon code expires?',
                'a': 'Promotional campaigns have strict start and end dates. Expired codes are automatically deactivated by our backend engine and cannot be applied.'
            }
        ]
    },
    {
        'category': 'Payments & Security',
        'icon': '🛡️',
        'questions': [
            {
                'q': 'What payment methods are supported on KARTMART?',
                'a': 'KARTMART supports Instant Simulated UPI (Google Pay, PhonePe, Paytm, QR), Simulated Debit & Credit Cards (Visa, Mastercard, RuPay), and Cash on Delivery (COD) at your doorstep.'
            },
            {
                'q': 'Is online payment simulation safe?',
                'a': 'Yes! Payment simulation is 100% safe and risk-free. No real financial charges occur on your cards or bank accounts during checkout.'
            }
        ]
    }
]


@support_bp.route('/help')
def help_center():
    return render_template(
        'support/help_center.html',
        faq_groups=FAQ_DATA,
        store_name=current_app.config.get('STORE_NAME', 'KARTMART')
    )


@support_bp.route('/help/ticket', methods=['POST'])
def submit_ticket():
    customer_name = request.form.get('customer_name', '').strip() or request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    category = request.form.get('category', 'Other')
    order_ref = request.form.get('order_ref', '').strip() or None
    subject = request.form.get('subject', '').strip()
    message = request.form.get('message', '').strip()

    if not customer_name or not email or not subject or not message:
        flash("Please fill in all required fields before submitting your inquiry.", "danger")
        return redirect(url_for('support.help_center'))

    ticket = SupportTicket(
        ticket_ref=SupportTicket.generate_ticket_ref(),
        user_id=session.get('user_id'),
        customer_name=customer_name,
        email=email,
        category=category,
        order_ref=order_ref,
        subject=subject,
        message=message,
        status='Open'
    )
    db.session.add(ticket)
    db.session.commit()

    flash(f"Support Ticket {ticket.ticket_ref} created! Our care team will reply to {email} within 24 hours.", "success")
    return redirect(url_for('support.help_center'))


@support_bp.route('/privacy')
def privacy():
    return render_template('support/privacy.html')


@support_bp.route('/terms')
def terms():
    return render_template('support/terms.html')
