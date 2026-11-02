from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, current_app
from app.extensions import db
from app.models import User, Address, WishlistItem, Order, Product
from app.services import CartService

account_bp = Blueprint('account', __name__, url_prefix='/account')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.args.get('format') == 'json':
                return jsonify({'status': 'unauthorized', 'message': 'Please sign in to continue'}), 200
            flash("Please sign in to access your account dashboard.", "info")
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@account_bp.route('/')
@account_bp.route('/profile')
@login_required
def profile():
    user = User.query.get_or_404(session['user_id'])
    addresses = user.addresses.order_by(Address.is_default.desc(), Address.id.desc()).all()
    orders_count = Order.query.filter_by(user_id=user.id).count()
    wishlist_count = WishlistItem.query.filter_by(user_id=user.id).count()
    recent_orders = Order.query.filter_by(user_id=user.id).order_by(Order.created_at.desc()).limit(3).all()

    return render_template(
        'account/profile.html',
        user=user,
        addresses=addresses,
        orders_count=orders_count,
        wishlist_count=wishlist_count,
        recent_orders=recent_orders,
        currency=current_app.config.get('CURRENCY_SYMBOL', '₹')
    )


@account_bp.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    user = User.query.get_or_404(session['user_id'])
    name = request.form.get('name', '').strip()
    phone = request.form.get('phone', '').strip()

    if not name:
        flash("Name cannot be empty.", "warning")
        return redirect(url_for('account.profile'))

    user.name = name
    user.phone = phone
    session['user_name'] = name
    db.session.commit()

    flash("Your profile details have been updated successfully.", "success")
    return redirect(url_for('account.profile'))


@account_bp.route('/addresses')
@login_required
def addresses():
    user = User.query.get_or_404(session['user_id'])
    address_list = user.addresses.order_by(Address.is_default.desc(), Address.id.desc()).all()

    return render_template(
        'account/addresses.html',
        user=user,
        addresses=address_list
    )


@account_bp.route('/addresses/add', methods=['POST'])
@login_required
def add_address():
    user_id = session['user_id']
    recipient_name = request.form.get('recipient_name', '').strip()
    phone = request.form.get('phone', '').strip()
    street_address = request.form.get('street_address', '').strip()
    landmark = request.form.get('landmark', '').strip()
    city = request.form.get('city', '').strip()
    state = request.form.get('state', '').strip() or 'Telangana'
    pincode = request.form.get('pincode', '').strip()
    address_type = request.form.get('address_type', 'Home')
    is_default = request.form.get('is_default') == 'on'

    if not recipient_name or not street_address or not city or not pincode:
        flash("Please fill in all required address fields.", "danger")
        return redirect(url_for('account.addresses'))

    # If this is the user's first address or marked default, unmark others
    if is_default or Address.query.filter_by(user_id=user_id).count() == 0:
        Address.query.filter_by(user_id=user_id).update({'is_default': False})
        is_default = True

    new_addr = Address(
        user_id=user_id,
        recipient_name=recipient_name,
        phone=phone,
        street_address=street_address,
        landmark=landmark,
        city=city,
        state=state,
        pincode=pincode,
        address_type=address_type,
        is_default=is_default
    )
    db.session.add(new_addr)
    db.session.commit()

    flash("New delivery address saved successfully!", "success")
    return redirect(url_for('account.addresses'))


@account_bp.route('/addresses/<int:addr_id>/set-default', methods=['POST'])
@login_required
def set_default_address(addr_id):
    user_id = session['user_id']
    target_addr = Address.query.filter_by(id=addr_id, user_id=user_id).first_or_404()

    Address.query.filter_by(user_id=user_id).update({'is_default': False})
    target_addr.is_default = True
    db.session.commit()

    flash(f"Default delivery address updated to '{target_addr.address_type}'.", "info")
    return redirect(url_for('account.addresses'))


@account_bp.route('/addresses/<int:addr_id>/delete', methods=['POST', 'GET'])
@account_bp.route('/addresses/delete/<int:addr_id>', methods=['POST', 'GET'])
@login_required
def delete_address(addr_id):
    user_id = session['user_id']
    target_addr = Address.query.filter_by(id=addr_id, user_id=user_id).first_or_404()

    db.session.delete(target_addr)
    db.session.commit()

    flash("Address deleted successfully.", "info")
    return redirect(url_for('account.addresses'))


@account_bp.route('/security', methods=['GET', 'POST'])
@login_required
def security():
    user = User.query.get_or_404(session['user_id'])

    if request.method == 'POST':
        current_pw = request.form.get('current_password', '')
        new_pw = request.form.get('new_password', '')
        confirm_pw = request.form.get('confirm_password', '')

        if not user.check_password(current_pw):
            flash("Current password is incorrect.", "danger")
            return redirect(url_for('account.security'))

        if len(new_pw) < 6:
            flash("New password must be at least 6 characters.", "danger")
            return redirect(url_for('account.security'))

        if new_pw != confirm_pw:
            flash("New passwords do not match.", "danger")
            return redirect(url_for('account.security'))

        user.set_password(new_pw)
        db.session.commit()
        flash("Password updated successfully! Please sign in with your new password.", "success")
        return redirect(url_for('account.profile'))

    return render_template('account/security.html', user=user)


@account_bp.route('/wishlist')
@login_required
def wishlist():
    user = User.query.get_or_404(session['user_id'])
    items = WishlistItem.query.filter_by(user_id=user.id).order_by(WishlistItem.created_at.desc()).all()

    return render_template(
        'account/wishlist.html',
        items=items,
        currency=current_app.config.get('CURRENCY_SYMBOL', '₹')
    )


@account_bp.route('/wishlist/toggle/<int:product_id>', methods=['POST', 'GET'])
@login_required
def toggle_wishlist(product_id):
    user_id = session['user_id']
    product = Product.query.get_or_404(product_id)

    existing = WishlistItem.query.filter_by(user_id=user_id, product_id=product_id).first()
    is_saved = False

    if existing:
        db.session.delete(existing)
        db.session.commit()
        msg = f"Removed '{product.name}' from your wishlist."
        is_saved = False
    else:
        new_item = WishlistItem(user_id=user_id, product_id=product_id)
        db.session.add(new_item)
        db.session.commit()
        msg = f"Added '{product.name}' to your wishlist!"
        is_saved = True

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.args.get('format') == 'json':
        count = WishlistItem.query.filter_by(user_id=user_id).count()
        return jsonify({
            'success': True,
            'is_saved': is_saved,
            'action': 'added' if is_saved else 'removed',
            'message': msg,
            'wishlist_count': count
        })

    flash(msg, "success" if is_saved else "info")
    return redirect(request.referrer or url_for('account.wishlist'))


@account_bp.route('/cancellations')
@login_required
def cancellations():
    user_id = session['user_id']
    cancelled_orders = Order.query.filter_by(user_id=user_id, order_status='Cancelled').order_by(Order.cancelled_at.desc()).all()

    return render_template(
        'account/cancellations.html',
        orders=cancelled_orders,
        currency=current_app.config.get('CURRENCY_SYMBOL', '₹')
    )
