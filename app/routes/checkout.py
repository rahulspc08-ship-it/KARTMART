import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from app.models import User, Product, Address
from app.services import CartService, OrderService, CouponService

checkout_bp = Blueprint('checkout', __name__, url_prefix='/checkout')


def _get_user_and_session():
    user_id = session.get('user_id')
    if not user_id:
        if 'guest_id' not in session:
            session['guest_id'] = f"guest_{uuid.uuid4().hex[:12]}"
        return None, session['guest_id']
    return user_id, None


@checkout_bp.route('/')
def index():
    user_id, session_id = _get_user_and_session()
    cart_data = CartService.get_cart_details(user_id=user_id, session_id=session_id)

    if not cart_data['items']:
        flash("Your shopping cart is empty. Add products before checking out.", "info")
        return redirect(url_for('products.catalogue'))

    # Pre-fill user profile info if logged in
    user = User.query.get(user_id) if user_id else None
    addresses = Address.query.filter_by(user_id=user.id).order_by(Address.is_default.desc()).all() if user else []

    # Check applied coupon from session
    applied_coupon = session.get('applied_coupon')
    discount_amount = 0.0
    if applied_coupon:
        discount_amount, _, _ = CouponService.validate_and_apply(applied_coupon, cart_data['subtotal'])

    final_total = max(round(cart_data['subtotal'] - discount_amount + cart_data['delivery_fee'], 2), 0.0)

    return render_template(
        'checkout.html',
        cart=cart_data,
        user=user,
        addresses=addresses,
        applied_coupon=applied_coupon,
        discount_amount=discount_amount,
        final_total=final_total,
        currency=current_app.config.get('CURRENCY_SYMBOL', '₹')
    )


@checkout_bp.route('/buy-now/<int:product_id>')
def buy_now(product_id):
    """Direct 1-click Buy Now flow: Adds product and routes directly to checkout."""
    user_id, session_id = _get_user_and_session()
    product = Product.query.get_or_404(product_id)

    if product.stock < 1:
        flash(f"Sorry, {product.name} is currently out of stock.", "warning")
        return redirect(url_for('products.detail', product_id=product_id))

    # Add to cart
    CartService.add_to_cart(product_id=product_id, quantity=1, user_id=user_id, session_id=session_id)
    return redirect(url_for('checkout.index'))


@checkout_bp.route('/apply-coupon', methods=['POST'])
def apply_coupon():
    code = request.form.get('coupon_code', '').strip().upper()
    user_id, session_id = _get_user_and_session()
    cart_data = CartService.get_cart_details(user_id=user_id, session_id=session_id)

    discount, coupon, msg = CouponService.validate_and_apply(code, cart_data['subtotal'])
    if coupon:
        session['applied_coupon'] = coupon.code
        flash(msg, "success")
    else:
        session.pop('applied_coupon', None)
        flash(msg, "danger")

    return redirect(url_for('checkout.index'))


@checkout_bp.route('/remove-coupon')
def remove_coupon():
    session.pop('applied_coupon', None)
    flash("Coupon removed.", "info")
    return redirect(url_for('checkout.index'))


@checkout_bp.route('/place-order', methods=['POST'])
def place_order():
    user_id, session_id = _get_user_and_session()
    cart_data = CartService.get_cart_details(user_id=user_id, session_id=session_id)

    if not cart_data['items']:
        flash("Your cart is empty.", "warning")
        return redirect(url_for('products.catalogue'))

    customer_data = {
        'customer_name': request.form.get('customer_name', '').strip(),
        'email': request.form.get('email', '').strip(),
        'phone': request.form.get('phone', '').strip(),
        'shipping_address': request.form.get('shipping_address', '').strip(),
        'city': request.form.get('city', '').strip(),
        'pincode': request.form.get('pincode', '').strip(),
        'payment_method': request.form.get('payment_method', 'Cash on Delivery')
    }

    # Validate required fields
    for field, val in customer_data.items():
        if not val:
            flash(f"Please fill in your {field.replace('_', ' ').capitalize()}.", "danger")
            return redirect(url_for('checkout.index'))

    applied_coupon = session.get('applied_coupon')

    order, err_msg = OrderService.create_order_from_cart(
        customer_data=customer_data,
        cart_items=cart_data['items'],
        user_id=user_id,
        coupon_code=applied_coupon
    )

    if not order:
        flash(f"Order placement failed: {err_msg}", "danger")
        return redirect(url_for('checkout.index'))

    # Empty the cart and clear coupon
    CartService.clear_cart(user_id=user_id, session_id=session_id)
    session.pop('applied_coupon', None)

    flash(f"🎉 Order {order.order_ref} placed successfully!", "success")
    return redirect(url_for('orders.success', order_ref=order.order_ref))
