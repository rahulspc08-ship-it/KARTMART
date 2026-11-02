from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from app.models import Order
from app.services import OrderService

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')


@orders_bp.route('/success/<order_ref>')
def success(order_ref):
    order = Order.query.filter_by(order_ref=order_ref).first_or_404()
    return render_template(
        'order_success.html',
        order=order,
        currency=current_app.config.get('CURRENCY_SYMBOL', '₹')
    )


@orders_bp.route('/')
def history():
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in to view your order history.", "info")
        return redirect(url_for('auth.login', next=url_for('orders.history')))

    orders = OrderService.get_user_orders(user_id)
    return render_template(
        'orders.html',
        orders=orders,
        currency=current_app.config.get('CURRENCY_SYMBOL', '₹')
    )


@orders_bp.route('/track/<order_ref>')
def track(order_ref):
    order = Order.query.filter_by(order_ref=order_ref).first_or_404()
    
    # Check permissions (either admin, or customer matching order email/user_id, or guest with ref)
    user_id = session.get('user_id')
    user_role = session.get('user_role')
    if order.user_id and order.user_id != user_id and user_role != 'admin':
        flash("You are not authorized to view this order.", "danger")
        return redirect(url_for('orders.history'))

    # Build status steps for visual timeline
    statuses = ['Placed', 'Confirmed', 'Shipped', 'Out for Delivery', 'Delivered']
    current_idx = statuses.index(order.order_status) if order.order_status in statuses else -1

    timeline = []
    for idx, s in enumerate(statuses):
        if order.order_status == 'Cancelled':
            state = 'cancelled' if s == 'Placed' else 'future'
        elif idx < current_idx:
            state = 'completed'
        elif idx == current_idx:
            state = 'active'
        else:
            state = 'future'
        timeline.append({'name': s, 'state': state})

    return render_template(
        'order_detail.html',
        order=order,
        timeline=timeline,
        currency=current_app.config.get('CURRENCY_SYMBOL', '₹')
    )


@orders_bp.route('/cancel/<order_ref>', methods=['GET', 'POST'])
def cancel(order_ref):
    order = Order.query.filter_by(order_ref=order_ref).first_or_404()
    user_id = session.get('user_id')
    is_admin = session.get('user_role') == 'admin'

    if order.user_id and order.user_id != user_id and not is_admin:
        flash("Unauthorized action.", "danger")
        return redirect(url_for('orders.history'))

    if request.method == 'POST':
        reason = request.form.get('cancellation_reason', '').strip()
        comments = request.form.get('cancellation_comments', '').strip()
        refund_method = request.form.get('refund_method', 'source')

        success, msg, _ = OrderService.cancel_order(
            order_id=order.id,
            user_id=user_id,
            reason=reason,
            comments=comments,
            refund_method=refund_method,
            is_admin=is_admin
        )

        if success:
            flash(msg, "info")
            return redirect(url_for('orders.cancel_success', order_ref=order.order_ref))
        else:
            flash(msg, "warning")
            return redirect(url_for('orders.cancel', order_ref=order.order_ref))

    return render_template(
        'order_cancel.html',
        order=order,
        reasons=OrderService.CANCELLATION_REASONS,
        currency=current_app.config.get('CURRENCY_SYMBOL', '₹')
    )


@orders_bp.route('/cancel-success/<order_ref>')
def cancel_success(order_ref):
    order = Order.query.filter_by(order_ref=order_ref).first_or_404()
    return render_template(
        'order_cancel_success.html',
        order=order,
        currency=current_app.config.get('CURRENCY_SYMBOL', '₹')
    )
