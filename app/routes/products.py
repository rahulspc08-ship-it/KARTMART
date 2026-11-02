from flask import Blueprint, render_template, request, current_app, session
from app.models import Product, Category, Coupon, Campaign, WishlistItem
from app.services import CouponService

products_bp = Blueprint('products', __name__)


def _get_user_wishlist_ids():
    user_id = session.get('user_id')
    if user_id:
        items = WishlistItem.query.filter_by(user_id=user_id).all()
        return {item.product_id for item in items}
    return set()


@products_bp.route('/')
def index():
    # Curated 12-13 main categories with genuine photographs
    main_slugs = [
        'electronics', 'mens-fashion', 'womens-fashion', 'kids-fashion',
        'toys-games', 'home-kitchen', 'furniture-decor', 'beauty-wellness',
        'sports-fitness', 'books-stationery', 'footwear', 'accessories-bags'
    ]
    categories = Category.query.filter(Category.slug.in_(main_slugs)).all()
    # Sort categories to preserve order
    categories.sort(key=lambda c: main_slugs.index(c.slug) if c.slug in main_slugs else 99)

    trending_products = Product.query.filter_by(is_active=True).order_by(Product.reviews_count.desc()).limit(8).all()
    most_loved_products = Product.query.filter_by(is_active=True).order_by(Product.rating.desc(), Product.id.asc()).limit(8).all()
    diwali_deals = Product.query.filter_by(is_active=True, is_diwali_deal=True).limit(6).all()
    
    active_campaign = Campaign.query.filter_by(is_active=True).first()
    active_coupons = CouponService.list_featured_coupons()
    wishlist_ids = _get_user_wishlist_ids()

    return render_template(
        'index.html',
        categories=categories,
        trending_products=trending_products,
        most_loved_products=most_loved_products,
        featured_products=trending_products,
        diwali_deals=diwali_deals,
        active_campaign=active_campaign,
        active_coupons=active_coupons,
        wishlist_ids=wishlist_ids,
        store_name=current_app.config.get('STORE_NAME', 'KARTMART'),
        tagline=current_app.config.get('STORE_TAGLINE', 'Next-Gen E-Commerce'),
        currency=current_app.config.get('CURRENCY_SYMBOL', '₹')
    )


@products_bp.route('/products')
def catalogue():
    search_query = request.args.get('q', '').strip()
    category_slug = request.args.get('category', '').strip()
    sort_by = request.args.get('sort', 'featured')
    diwali_filter = request.args.get('festive') == 'true'

    query = Product.query.filter_by(is_active=True)

    selected_category = None
    if category_slug:
        selected_category = Category.query.filter_by(slug=category_slug).first()
        if selected_category:
            query = query.filter_by(category_id=selected_category.id)

    if diwali_filter:
        query = query.filter_by(is_diwali_deal=True)

    if search_query:
        query = query.filter(
            (Product.name.ilike(f'%{search_query}%')) | 
            (Product.description.ilike(f'%{search_query}%')) |
            (Product.brand.ilike(f'%{search_query}%'))
        )

    if sort_by == 'price_low':
        query = query.order_by(Product.price.asc())
    elif sort_by == 'price_high':
        query = query.order_by(Product.price.desc())
    elif sort_by == 'rating':
        query = query.order_by(Product.rating.desc())
    else:
        query = query.order_by(Product.id.asc())

    products = query.all()
    categories = Category.query.order_by(Category.name.asc()).all()
    wishlist_ids = _get_user_wishlist_ids()

    return render_template(
        'catalogue.html',
        products=products,
        categories=categories,
        selected_category=selected_category,
        search_query=search_query,
        sort_by=sort_by,
        diwali_filter=diwali_filter,
        wishlist_ids=wishlist_ids,
        currency=current_app.config.get('CURRENCY_SYMBOL', '₹')
    )


@products_bp.route('/product/<int:product_id>')
def detail(product_id):
    product = Product.query.get_or_404(product_id)
    related_products = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id,
        Product.is_active.is_(True)
    ).limit(4).all()

    # Group variants by type (e.g. Color, Size)
    variants_by_type = {}
    for v in product.variants:
        variants_by_type.setdefault(v.variant_type, []).append(v)

    wishlist_ids = _get_user_wishlist_ids()
    is_in_wishlist = product.id in wishlist_ids

    return render_template(
        'product_detail.html',
        product=product,
        variants_by_type=variants_by_type,
        related_products=related_products,
        is_in_wishlist=is_in_wishlist,
        currency=current_app.config.get('CURRENCY_SYMBOL', '₹')
    )
