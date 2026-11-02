from datetime import datetime, timedelta
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from app.extensions import db
from app.models import Order, Product, Category, User, Campaign, Coupon, SupportTicket
from app.services import OrderService, InventoryService

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id') or session.get('user_role') != 'admin':
            flash("Administrator access required. Please log in as Admin.", "danger")
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/login')
def login_redirect():
    return redirect(url_for('auth.admin_login', next=request.args.get('next')))


@admin_bp.route('/register')
def register_redirect():
    return redirect(url_for('auth.admin_register'))


@admin_bp.route('', strict_slashes=False)
@admin_bp.route('/', strict_slashes=False)
@admin_required
def dashboard():
    total_orders = Order.query.count()
    completed_orders = Order.query.filter(Order.order_status.in_(['Confirmed', 'Shipped', 'Out for Delivery', 'Delivered'])).all()
    total_sales = sum(o.total_amount for o in completed_orders)
    pending_orders_count = Order.query.filter_by(order_status='Placed').count()
    cancelled_orders_count = Order.query.filter_by(order_status='Cancelled').count()
    active_products = Product.query.filter_by(is_active=True).count()
    low_stock = InventoryService.get_low_stock_items(threshold=5)
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    active_campaigns = Campaign.query.filter_by(is_active=True).all()
    open_tickets_count = SupportTicket.query.filter_by(status='Open').count()

    return render_template(
        'admin/dashboard.html',
        total_orders=total_orders,
        total_sales=round(total_sales, 2),
        pending_orders_count=pending_orders_count,
        cancelled_orders_count=cancelled_orders_count,
        active_products=active_products,
        low_stock=low_stock,
        recent_orders=recent_orders,
        active_campaigns=active_campaigns,
        open_tickets_count=open_tickets_count,
        currency=current_app.config.get('CURRENCY_SYMBOL', '₹')
    )


@admin_bp.route('/orders')
@admin_required
def orders():
    status_filter = request.args.get('status', 'all')
    query = Order.query.order_by(Order.created_at.desc())
    if status_filter != 'all':
        query = query.filter_by(order_status=status_filter)
        
    all_orders = query.all()
    return render_template(
        'admin/orders.html',
        orders=all_orders,
        status_filter=status_filter,
        currency=current_app.config.get('CURRENCY_SYMBOL', '₹')
    )


@admin_bp.route('/cancellations')
@admin_required
def cancellations():
    cancelled_orders = Order.query.filter_by(order_status='Cancelled').order_by(Order.cancelled_at.desc()).all()
    return render_template(
        'admin/cancellations.html',
        orders=cancelled_orders,
        currency=current_app.config.get('CURRENCY_SYMBOL', '₹')
    )


@admin_bp.route('/order/<int:order_id>/status', methods=['POST'])
@admin_required
def update_status(order_id):
    new_status = request.form.get('order_status')
    success, msg = OrderService.update_status(order_id, new_status)
    if success:
        flash(msg, "success")
    else:
        flash(msg, "warning")
    return redirect(request.referrer or url_for('admin.orders'))


@admin_bp.route('/products')
@admin_required
def products():
    all_products = Product.query.order_by(Product.id.asc()).all()
    categories = Category.query.all()
    return render_template(
        'admin/products.html',
        products=all_products,
        categories=categories,
        currency=current_app.config.get('CURRENCY_SYMBOL', '₹')
    )


@admin_bp.route('/product/add', methods=['POST'])
@admin_required
def add_product():
    name = request.form.get('name', '').strip()
    category_id = int(request.form.get('category_id'))
    brand = request.form.get('brand', '').strip()
    price = float(request.form.get('price', 0.0))
    original_price = float(request.form.get('original_price', 0.0)) or None
    stock = int(request.form.get('stock', 10))
    image_url = request.form.get('image_url', '').strip() or '/static/img/products/headphones.jpg'
    badge = request.form.get('badge', '').strip() or None
    is_diwali_deal = request.form.get('is_diwali_deal') == 'on'
    description = request.form.get('description', '').strip()

    if not name or price <= 0:
        flash("Valid product name and price are required.", "danger")
        return redirect(url_for('admin.products'))

    product = Product(
        name=name,
        category_id=category_id,
        brand=brand,
        price=price,
        original_price=original_price,
        stock=stock,
        image_url=image_url,
        badge=badge,
        is_diwali_deal=is_diwali_deal,
        description=description,
        is_active=True
    )
    db.session.add(product)
    db.session.commit()

    flash(f"Product '{product.name}' added successfully!", "success")
    return redirect(url_for('admin.products'))


@admin_bp.route('/product/<int:product_id>/restock', methods=['POST'])
@admin_required
def restock(product_id):
    product = Product.query.get_or_404(product_id)
    add_qty = int(request.form.get('quantity', 10))
    product.stock += add_qty
    db.session.commit()
    flash(f"Restocked {product.name} by +{add_qty} units (Total: {product.stock})", "success")
    return redirect(request.referrer or url_for('admin.products'))


@admin_bp.route('/campaigns')
@admin_required
def campaigns():
    all_campaigns = Campaign.query.order_by(Campaign.created_at.desc()).all()
    all_coupons = Coupon.query.order_by(Coupon.id.desc()).all()
    return render_template(
        'admin/campaigns.html',
        campaigns=all_campaigns,
        coupons=all_coupons,
        currency=current_app.config.get('CURRENCY_SYMBOL', '₹')
    )


@admin_bp.route('/campaign/add', methods=['POST'])
@admin_required
def add_campaign():
    title = request.form.get('title', '').strip()
    slug = request.form.get('slug', '').strip().lower().replace(' ', '-')
    badge = request.form.get('badge', 'FESTIVE SALE').strip()
    headline = request.form.get('headline', '').strip()
    description = request.form.get('description', '').strip()
    discount_text = request.form.get('discount_text', '').strip()
    days = int(request.form.get('duration_days', 15))

    now = datetime.utcnow()
    campaign = Campaign(
        title=title,
        slug=slug,
        badge=badge,
        headline=headline,
        description=description,
        discount_text=discount_text,
        start_date=now,
        end_date=now + timedelta(days=days),
        is_active=True,
        banner_image='/static/img/products/diwali_banner.jpg'
    )
    db.session.add(campaign)
    db.session.commit()

    flash(f"Promotional Campaign '{campaign.title}' created and activated!", "success")
    return redirect(url_for('admin.campaigns'))


@admin_bp.route('/coupon/add', methods=['POST'])
@admin_required
def add_coupon():
    code = request.form.get('code', '').strip().upper()
    discount_type = request.form.get('discount_type', 'percentage')
    discount_percent = int(request.form.get('discount_percent', 10))
    max_discount = float(request.form.get('max_discount', 1000.0))
    min_order_amount = float(request.form.get('min_order_amount', 0.0))
    description = request.form.get('description', '').strip()
    days = int(request.form.get('duration_days', 30))

    now = datetime.utcnow()
    coupon = Coupon(
        code=code,
        discount_type=discount_type,
        discount_percent=discount_percent if discount_type == 'percentage' else 0,
        max_discount=max_discount,
        min_order_amount=min_order_amount,
        description=description,
        start_date=now,
        end_date=now + timedelta(days=days),
        is_active=True
    )
    db.session.add(coupon)
    db.session.commit()

    flash(f"Coupon '{coupon.code}' created with {days} days validity!", "success")
    return redirect(url_for('admin.campaigns'))


@admin_bp.route('/coupon/<int:coupon_id>/toggle', methods=['POST'])
@admin_required
def toggle_coupon(coupon_id):
    coupon = Coupon.query.get_or_404(coupon_id)
    coupon.is_active = not coupon.is_active
    db.session.commit()
    flash(f"Coupon {coupon.code} status set to {'Active' if coupon.is_active else 'Deactivated'}.", "info")
    return redirect(url_for('admin.campaigns'))


@admin_bp.route('/support')
@admin_required
def support():
    tickets = SupportTicket.query.order_by(SupportTicket.created_at.desc()).all()
    return render_template('admin/support.html', tickets=tickets)


@admin_bp.route('/support/<int:ticket_id>/resolve', methods=['POST'])
@admin_required
def resolve_ticket(ticket_id):
    ticket = SupportTicket.query.get_or_404(ticket_id)
    ticket.status = 'Resolved'
    ticket.admin_response = request.form.get('admin_response', 'Inquiry resolved by customer care specialist.')
    db.session.commit()
    flash(f"Ticket {ticket.ticket_ref} marked as Resolved.", "success")
    return redirect(url_for('admin.support'))
