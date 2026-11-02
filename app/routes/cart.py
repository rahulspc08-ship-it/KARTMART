import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, current_app
from app.services import CartService

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')


def _get_user_and_session():
    user_id = session.get('user_id')
    if not user_id:
        if 'guest_id' not in session:
            session['guest_id'] = f"guest_{uuid.uuid4().hex[:12]}"
        return None, session['guest_id']
    return user_id, None


@cart_bp.route('/')
def view():
    user_id, session_id = _get_user_and_session()
    cart_data = CartService.get_cart_details(user_id=user_id, session_id=session_id)
    
    return render_template(
        'cart.html',
        cart=cart_data,
        currency=current_app.config.get('CURRENCY_SYMBOL', '₹')
    )


@cart_bp.route('/add/<int:product_id>', methods=['POST', 'GET'])
def add(product_id):
    user_id, session_id = _get_user_and_session()
    quantity = int(request.form.get('quantity', 1) if request.method == 'POST' else request.args.get('quantity', 1))

    success, message = CartService.add_to_cart(
        product_id=product_id,
        quantity=quantity,
        user_id=user_id,
        session_id=session_id
    )

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.args.get('format') == 'json'

    if is_ajax:
        cart_data = CartService.get_cart_details(user_id=user_id, session_id=session_id)
        return jsonify({
            'success': success,
            'message': message,
            'cart_count': cart_data['total_items'],
            'cart_subtotal': cart_data['subtotal']
        })

    if success:
        flash(message, "success")
    else:
        flash(message, "warning")

    return redirect(request.referrer or url_for('cart.view'))


@cart_bp.route('/update/<int:item_id>', methods=['POST'])
def update(item_id):
    user_id, session_id = _get_user_and_session()
    quantity = int(request.form.get('quantity', 1))

    success, message = CartService.update_quantity(
        cart_item_id=item_id,
        quantity=quantity,
        user_id=user_id,
        session_id=session_id
    )

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart_data = CartService.get_cart_details(user_id=user_id, session_id=session_id)
        return jsonify({
            'success': success,
            'message': message,
            'cart_count': cart_data['total_items'],
            'cart_subtotal': cart_data['subtotal'],
            'cart_total': cart_data['total']
        })

    flash(message, "info" if success else "warning")
    return redirect(url_for('cart.view'))


@cart_bp.route('/remove/<int:item_id>')
def remove(item_id):
    user_id, session_id = _get_user_and_session()
    CartService.remove_item(item_id, user_id=user_id, session_id=session_id)
    flash("Item removed from cart.", "info")
    return redirect(url_for('cart.view'))


@cart_bp.route('/clear')
def clear():
    user_id, session_id = _get_user_and_session()
    CartService.clear_cart(user_id=user_id, session_id=session_id)
    flash("Your shopping cart has been cleared.", "info")
    return redirect(url_for('cart.view'))


@cart_bp.route('/api/drawer')
def drawer_api():
    """Returns real-time cart data for slide-out cart drawer."""
    user_id, session_id = _get_user_and_session()
    cart_data = CartService.get_cart_details(user_id=user_id, session_id=session_id)
    return jsonify({
        'total_items': cart_data['total_items'],
        'subtotal': cart_data['subtotal'],
        'delivery_fee': cart_data['delivery_fee'],
        'total': cart_data['total'],
        'items': [item.to_dict() for item in cart_data['items']]
    })
