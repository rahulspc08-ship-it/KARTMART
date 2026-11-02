import os
import uuid
from flask import Flask, session
from app.config import config_by_name
from app.extensions import db
from app.services import CartService


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    config_class = config_by_name.get(config_name, config_by_name['default'])

    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static'
    )
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # Context processor to make cart count and user available to all templates
    @app.context_processor
    def inject_global_data():
        user_id = session.get('user_id')
        session_id = session.get('guest_id')
        cart_count = 0
        try:
            if user_id or session_id:
                cart_data = CartService.get_cart_details(user_id=user_id, session_id=session_id)
                cart_count = cart_data['total_items']
        except Exception:
            cart_count = 0

        return {
            'global_cart_count': cart_count,
            'is_logged_in': bool(user_id),
            'logged_in_user': session.get('user_name'),
            'is_admin': session.get('user_role') == 'admin',
            'currency': app.config.get('CURRENCY_SYMBOL', '₹'),
            'store_name': app.config.get('STORE_NAME', 'KARTMART')
        }

    # Register Blueprints
    from app.routes import (
        auth_bp,
        products_bp,
        cart_bp,
        checkout_bp,
        orders_bp,
        admin_bp,
        api_bp,
        account_bp,
        support_bp
    )

    app.register_blueprint(products_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(checkout_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(account_bp)
    app.register_blueprint(support_bp)

    # Backward-compatible alias for root /health
    @app.route('/health')
    def health_redirect():
        from app.routes.api import health
        return health()

    # Create tables automatically within app context if using sqlite
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            app.logger.warning(f"Database table initialization notice: {e}")

    return app
