import pytest
from datetime import datetime, timedelta
from app import create_app
from app.extensions import db
from app.models import User, Category, Product, Coupon, CartItem, Order, Address, WishlistItem, SupportTicket
from app.services import CartService, OrderService, CouponService


@pytest.fixture
def app():
    """Create and configure an isolated in-memory app instance for testing."""
    test_app = create_app('testing')

    with test_app.app_context():
        db.create_all()

        # Seed minimal test fixtures
        cat = Category(name='Electronics', slug='electronics', icon='⚡', description='Tech gadgets')
        db.session.add(cat)
        db.session.flush()

        prod = Product(
            name='Test Smartphone Pro',
            description='Test high performance smartphone',
            price=24999.00,
            original_price=29999.00,
            stock=10,
            category_id=cat.id,
            rating=4.8,
            reviews_count=25,
            badge='Bestseller',
            emoji='📱',
            image_url='/static/img/products/smartphone.jpg',
            is_diwali_deal=True,
            is_featured=True
        )
        db.session.add(prod)

        coupon = Coupon(
            code='DIWALI50',
            discount_percent=50,
            max_discount=1500.0,
            min_order_amount=999.0,
            is_active=True,
            description='Diwali 50% discount'
        )
        db.session.add(coupon)

        expired_coupon = Coupon(
            code='EXPIREDTEST',
            discount_percent=20,
            max_discount=500.0,
            min_order_amount=500.0,
            is_active=True,
            start_date=datetime.utcnow() - timedelta(days=30),
            end_date=datetime.utcnow() - timedelta(days=1),
            description='Expired coupon'
        )
        db.session.add(expired_coupon)

        admin = User(
            name='Admin User',
            email='admin@kartmart.local',
            role='admin'
        )
        admin.set_password('Admin@123')
        db.session.add(admin)

        customer = User(
            name='Rahul Customer',
            email='customer@kartmart.local',
            role='customer'
        )
        customer.set_password('Customer@123')
        db.session.add(customer)

        db.session.commit()

        yield test_app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_app_config(app):
    """Test configuration in testing environment."""
    assert app.config['TESTING'] is True
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:'


def test_health_endpoints(client):
    """Verify health endpoints return structured JSON status."""
    for path in ['/api/health', '/health']:
        res = client.get(path)
        assert res.status_code == 200
        data = res.get_json()
        assert data['application'] == 'KARTMART'
        assert data['database']['status'] == 'connected'
        assert data['status'] == 'healthy'


def test_storefront_and_catalogue(client):
    """Verify storefront index and product catalogue render successfully."""
    # Home Page
    res = client.get('/')
    assert res.status_code == 200
    assert b'KART' in res.data
    assert b'Test Smartphone Pro' in res.data
    assert b'Trending Products' in res.data
    assert b'Most Loved Products' in res.data

    # Catalogue Page
    cat_res = client.get('/products')
    assert cat_res.status_code == 200
    assert b'All 13 Categories' in cat_res.data
    assert b'Test Smartphone Pro' in cat_res.data

    # Product Detail Page
    detail_res = client.get('/product/1')
    assert detail_res.status_code == 200
    assert b'Test Smartphone Pro' in detail_res.data
    assert b'Add to Bag' in detail_res.data
    assert b'Buy Now' in detail_res.data


def test_user_registration_and_login(client):
    """Verify customer registration, password hashing, and authentication."""
    reg_res = client.post('/auth/register', data={
        'name': 'Pooja Reddy',
        'email': 'pooja@test.local',
        'password': 'SecurePassword123',
        'confirm_password': 'SecurePassword123',
        'phone': '9876543211',
        'address': 'Madhapur, Hitech City',
        'city': 'Hyderabad',
        'pincode': '500081'
    }, follow_redirects=True)
    assert reg_res.status_code == 200

    with client.session_transaction() as sess:
        assert sess.get('user_id') is not None
        assert sess.get('user_name') == 'Pooja Reddy'


def test_demo_logins(client):
    """Verify 1-click evaluator demo login routes for customer and admin."""
    # Demo Customer
    res_cust = client.get('/auth/demo-login/customer', follow_redirects=True)
    assert res_cust.status_code == 200
    with client.session_transaction() as sess:
        assert sess.get('user_role') == 'customer'
        assert sess.get('user_email') == 'customer@kartmart.local'

    # Demo Admin
    res_admin = client.get('/auth/demo-login/admin', follow_redirects=True)
    assert res_admin.status_code == 200
    with client.session_transaction() as sess:
        assert sess.get('user_role') == 'admin'
        assert sess.get('user_email') == 'admin@kartmart.local'


def test_cart_operations_and_drawer_api(client):
    """Verify adding items to cart and slide-out cart drawer JSON API."""
    add_res = client.post('/cart/add/1?format=json', headers={'X-Requested-With': 'XMLHttpRequest'})
    assert add_res.status_code == 200
    data = add_res.get_json()
    assert data['success'] is True
    assert data['cart_count'] == 1

    drawer_res = client.get('/cart/api/drawer')
    assert drawer_res.status_code == 200
    drawer_data = drawer_res.get_json()
    assert drawer_data['total_items'] == 1
    assert len(drawer_data['items']) == 1
    assert drawer_data['items'][0]['product_name'] == 'Test Smartphone Pro'
    assert drawer_data['items'][0]['product_image'] is not None
    assert drawer_data['subtotal'] == 24999.00


def test_coupon_validation_and_application(client):
    """Verify promo code validation service and API."""
    # Active valid coupon
    valid_res = client.get('/api/coupon/validate?code=DIWALI50&order_total=2000')
    assert valid_res.status_code == 200
    vdata = valid_res.get_json()
    assert vdata['valid'] is True
    assert vdata['discount_amount'] == 1000.0

    # Expired coupon should be rejected
    exp_res = client.get('/api/coupon/validate?code=EXPIREDTEST&order_total=2000')
    assert exp_res.status_code == 200
    exp_data = exp_res.get_json()
    assert exp_data['valid'] is False
    assert 'expired' in exp_data['message'].lower()


def test_buy_now_flow(client):
    """Verify 1-click '⚡ Buy Now' button directly transitions to checkout."""
    res = client.get('/checkout/buy-now/1', follow_redirects=True)
    assert res.status_code == 200
    assert b'Checkout' in res.data
    assert b'Delivery Address' in res.data
    assert b'Payment Method' in res.data
    assert b'Test Smartphone Pro' in res.data


def test_checkout_and_place_order(client):
    """Verify complete checkout workflow and transactional order placement."""
    client.get('/auth/demo-login/customer')
    client.post('/cart/add/1')
    client.post('/checkout/apply-coupon', data={'coupon_code': 'DIWALI50'}, follow_redirects=True)

    order_res = client.post('/checkout/place-order', data={
        'customer_name': 'Rahul Sharma',
        'phone': '9812345678',
        'email': 'customer@kartmart.local',
        'shipping_address': 'Flat 402, Green Valley Apartments',
        'city': 'Hyderabad',
        'pincode': '500034',
        'payment_method': 'Simulated UPI'
    }, follow_redirects=True)

    assert order_res.status_code == 200
    assert b'ORDER CONFIRMED' in order_res.data
    assert b'KART-' in order_res.data
    assert b'Simulated UPI' in order_res.data


def test_order_cancellation_workflow(client, app):
    """Verify multi-step order cancellation, reason validation, and inventory replenishment."""
    client.get('/auth/demo-login/customer')
    client.post('/cart/add/1')

    # Place order
    client.post('/checkout/place-order', data={
        'customer_name': 'Rahul Sharma',
        'phone': '9812345678',
        'email': 'customer@kartmart.local',
        'shipping_address': 'Flat 402, Green Valley Apartments',
        'city': 'Hyderabad',
        'pincode': '500034',
        'payment_method': 'Cash on Delivery'
    }, follow_redirects=True)

    with app.app_context():
        order = Order.query.filter_by(email='customer@kartmart.local').first()
        assert order is not None
        order_ref = str(order.order_ref)
        p = db.session.get(Product, 1)
        initial_stock = int(p.stock)

    # View cancellation page
    cancel_page_res = client.get(f'/orders/cancel/{order_ref}')
    assert cancel_page_res.status_code == 200
    assert b'Cancel Order' in cancel_page_res.data
    assert b'Ordered by mistake' in cancel_page_res.data

    # Submit cancellation
    post_res = client.post(f'/orders/cancel/{order_ref}', data={
        'cancellation_reason': 'Ordered by mistake',
        'cancellation_comments': 'Accidentally added to cart',
        'refund_destination': 'Original Payment Method'
    }, follow_redirects=True)

    assert post_res.status_code == 200
    assert b'ORDER CANCELLED' in post_res.data

    with app.app_context():
        refreshed_order = Order.query.filter_by(order_ref=order_ref).first()
        assert refreshed_order.order_status == 'Cancelled'
        assert refreshed_order.cancellation_reason == 'Ordered by mistake'
        assert refreshed_order.cancellation_comments == 'Accidentally added to cart'
        assert refreshed_order.cancelled_at is not None
        # Verify inventory replenished
        p_updated = db.session.get(Product, 1)
        assert p_updated.stock == initial_stock + 1


def test_order_cancellation_blocked_when_shipped(client, app):
    """Verify order cancellation is strictly blocked if order is Shipped or Delivered."""
    client.get('/auth/demo-login/customer')
    client.post('/cart/add/1')

    client.post('/checkout/place-order', data={
        'customer_name': 'Rahul Sharma',
        'phone': '9812345678',
        'email': 'customer@kartmart.local',
        'shipping_address': 'Flat 402, Green Valley Apartments',
        'city': 'Hyderabad',
        'pincode': '500034',
        'payment_method': 'Cash on Delivery'
    }, follow_redirects=True)

    with app.app_context():
        order = Order.query.filter_by(email='customer@kartmart.local').first()
        order.order_status = 'Shipped'
        db.session.commit()
        order_ref = str(order.order_ref)

    # Cancellation page should show blocked state
    res = client.get(f'/orders/cancel/{order_ref}')
    assert res.status_code == 200
    assert b'Order Cannot Be Cancelled' in res.data

    # POST attempt should fail
    post_res = client.post(f'/orders/cancel/{order_ref}', data={
        'cancellation_reason': 'Ordered by mistake'
    }, follow_redirects=True)
    assert b'cannot be cancelled' in post_res.data


def test_wishlist_toggle(client):
    """Verify saved wishlist item toggle and JSON response."""
    # Unauthenticated -> returns 200 with unauthorized status for AJAX
    anon_res = client.post('/account/wishlist/toggle/1', headers={'X-Requested-With': 'XMLHttpRequest'})
    assert anon_res.status_code == 200
    assert anon_res.get_json()['status'] == 'unauthorized'

    # Authenticate
    client.get('/auth/demo-login/customer')

    # Add to wishlist
    add_res = client.post('/account/wishlist/toggle/1', headers={'X-Requested-With': 'XMLHttpRequest'})
    assert add_res.status_code == 200
    add_data = add_res.get_json()
    assert add_data['action'] == 'added'

    # Remove from wishlist
    rem_res = client.post('/account/wishlist/toggle/1', headers={'X-Requested-With': 'XMLHttpRequest'})
    assert rem_res.status_code == 200
    rem_data = rem_res.get_json()
    assert rem_data['action'] == 'removed'


def test_support_ticket_submission(client, app):
    """Verify customer support ticket submission with auto-generated ticket ref."""
    client.get('/auth/demo-login/customer')

    res = client.post('/help/ticket', data={
        'name': 'Rahul Customer',
        'email': 'customer@kartmart.local',
        'category': 'Order Cancellation & Refund',
        'order_ref': 'KART-TEST',
        'subject': 'Question regarding refund timeline',
        'message': 'When will the refunded amount appear in my account?'
    }, follow_redirects=True)

    assert res.status_code == 200
    assert b'Support Ticket' in res.data
    assert b'TICK-' in res.data

    with app.app_context():
        ticket = SupportTicket.query.filter_by(email='customer@kartmart.local').first()
        assert ticket is not None
        assert ticket.ticket_ref.startswith('TICK-')
        assert ticket.category == 'Order Cancellation & Refund'


def test_address_book_crud(client, app):
    """Verify customer address management (create, set default, delete)."""
    client.get('/auth/demo-login/customer')

    # Add address
    add_res = client.post('/account/addresses/add', data={
        'recipient_name': 'Rahul Sharma Office',
        'phone': '9876543210',
        'street_address': 'Building 14, Mindspace IT Park',
        'landmark': 'Near Inorbit Mall',
        'city': 'Hyderabad',
        'state': 'Telangana',
        'pincode': '500081',
        'address_type': 'Work',
        'is_default': 'y'
    }, follow_redirects=True)

    assert add_res.status_code == 200
    assert b'New delivery address saved' in add_res.data

    with app.app_context():
        addr = Address.query.filter_by(recipient_name='Rahul Sharma Office').first()
        assert addr is not None
        assert addr.is_default is True
        addr_id = addr.id

    # Delete address
    del_res = client.post(f'/account/addresses/delete/{addr_id}', follow_redirects=True)
    assert del_res.status_code == 200
    assert b'Address deleted successfully' in del_res.data


def test_admin_access_control(client):
    """Verify admin route protection against unauthorized customers."""
    res_anon = client.get('/admin')
    assert res_anon.status_code == 302
    assert '/auth/login' in res_anon.headers['Location']

    client.get('/auth/demo-login/customer')
    res_cust = client.get('/admin', follow_redirects=True)
    assert b'Administrator access required' in res_cust.data

    client.get('/auth/demo-login/admin')
    res_admin = client.get('/admin')
    assert res_admin.status_code == 200
    assert b'ADMINISTRATOR CONSOLE' in res_admin.data


def test_admin_portal_login_and_registration(client):
    """Verify dedicated admin portal login and secure key-protected registration."""
    # Test GET routes
    res_get_login = client.get('/auth/admin/login')
    assert res_get_login.status_code == 200
    assert b'Administrator Portal' in res_get_login.data

    res_get_reg = client.get('/auth/admin/register')
    assert res_get_reg.status_code == 200
    assert b'Create Administrator Account' in res_get_reg.data

    # Test registration with invalid key
    res_bad_key = client.post('/auth/admin/register', data={
        'name': 'Fraudulent Admin',
        'email': 'hacker@example.com',
        'password': 'password123',
        'confirm_password': 'password123',
        'admin_key': 'wrong_key'
    }, follow_redirects=True)
    assert b'Invalid Admin Security Key' in res_bad_key.data

    # Test registration with valid key
    res_success_reg = client.post('/auth/admin/register', data={
        'name': 'Chief Admin Officer',
        'email': 'officer@kartmart.local',
        'password': 'AdminPassword@123',
        'confirm_password': 'AdminPassword@123',
        'admin_key': 'Admin@2026'
    }, follow_redirects=True)
    assert res_success_reg.status_code == 200
    assert b'ADMINISTRATOR CONSOLE' in res_success_reg.data

    with client.session_transaction() as sess:
        assert sess.get('user_role') == 'admin'
        assert sess.get('user_email') == 'officer@kartmart.local'

    # Test logout and admin portal login
    client.get('/auth/logout')
    res_login = client.post('/auth/admin/login', data={
        'email': 'officer@kartmart.local',
        'password': 'AdminPassword@123'
    }, follow_redirects=True)
    assert res_login.status_code == 200
    assert b'ADMINISTRATOR CONSOLE' in res_login.data
