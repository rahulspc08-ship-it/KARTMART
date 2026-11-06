from flask import Blueprint, jsonify, current_app, request
from sqlalchemy import text
from app.extensions import db
from app.services import CouponService

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/health')
def health():
    db_status = 'disconnected'
    db_error = None
    try:
        with db.engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        db_status = 'connected'
    except Exception as e:
        db_status = 'unavailable'
        db_error = str(e)

    db_uri = current_app.config.get('SQLALCHEMY_DATABASE_URI', '')
    engine_name = 'mysql' if 'mysql' in db_uri else ('sqlite' if 'sqlite' in db_uri else 'unknown')

    return jsonify({
        'status': 'healthy' if db_status == 'connected' else 'degraded',
        'application': 'KARTMART',
        'environment': current_app.config.get('ENV', 'development'),
        'database': {
            'status': db_status,
            'engine': engine_name,
            'error': db_error
        }
    })


@api_bp.route('/coupon/validate', methods=['GET', 'POST'])
def validate_coupon():
    if request.method == 'POST':
        data = request.get_json(silent=True) or request.form
        code = data.get('code', '')
        subtotal = float(data.get('subtotal', data.get('order_total', 0.0)))
    else:
        code = request.args.get('code', '')
        subtotal = float(request.args.get('subtotal', request.args.get('order_total', 0.0)))

    discount, coupon, msg = CouponService.validate_and_apply(code, subtotal)

    if coupon:
        return jsonify({
            'valid': True,
            'code': coupon.code,
            'discount': discount,
            'discount_amount': discount,
            'percent': coupon.discount_percent,
            'message': msg
        })
    return jsonify({
        'valid': False,
        'discount': 0.0,
        'discount_amount': 0.0,
        'message': msg
    })


@api_bp.route('/seed', methods=['GET', 'POST'])
def trigger_seed():
    """Trigger or re-seed the catalog and demo accounts."""
    from app.models import Product
    current_count = Product.query.count()
    key = request.args.get('key', '')
    expected_key = current_app.config.get('ADMIN_REGISTRATION_KEY', 'Admin@2026')

    # Allow without key if database is empty, require key if already seeded
    if current_count > 0 and key != expected_key:
        return jsonify({
            'success': False,
            'products_count': current_count,
            'message': f'Database already has {current_count} products. Provide ?key={expected_key} to re-seed.'
        }), 200

    from seed_db import seed_database
    from seed_catalog_expanded import seed_expanded_catalog
    seed_database()
    seed_expanded_catalog()
    new_count = Product.query.count()
    return jsonify({
        'success': True,
        'products_count': new_count,
        'message': f'Successfully seeded database with {new_count} products across 13 categories.'
    })
