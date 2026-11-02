from flask import Blueprint, render_template, jsonify, current_app
from sqlalchemy import text
from . import db

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Home page route displaying hero banner and store overview."""
    db_uri = current_app.config.get('SQLALCHEMY_DATABASE_URI', '')
    # Mask credentials if MySQL URI
    if '@' in db_uri:
        db_type = 'MySQL'
        db_masked = db_uri.split('@')[-1]
    else:
        db_type = 'SQLite' if 'sqlite' in db_uri else 'Database'
        db_masked = 'Local instance'
        
    categories = [
        {'id': 'electronics', 'name': 'Electronics', 'icon': '⚡', 'description': 'Gadgets, audio, accessories & computing'},
        {'id': 'clothing', 'name': 'Clothing', 'icon': '👔', 'description': 'Curated fashion for everyday lifestyle'},
        {'id': 'accessories', 'name': 'Accessories', 'icon': '⌚', 'description': 'Timepieces, bags, and modern essentials'},
        {'id': 'books', 'name': 'Books', 'icon': '📚', 'description': 'Bestsellers, tech guides & fiction'},
        {'id': 'home', 'name': 'Home Products', 'icon': '🏡', 'description': 'Decor, kitchenware, and smart living'}
    ]
    
    return render_template(
        'index.html',
        store_name=current_app.config.get('STORE_NAME', 'KARTMART'),
        tagline=current_app.config.get('STORE_TAGLINE', 'Next-Gen E-Commerce'),
        categories=categories,
        db_type=db_type,
        db_masked=db_masked
    )


@main_bp.route('/health')
def health_check():
    """Safe health check route checking application and database connection."""
    db_status = 'disconnected'
    db_error = None
    
    try:
        # Perform safe read-only ping
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
