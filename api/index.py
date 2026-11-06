import os
import sys

# Add project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db

app = create_app()

# Auto-create tables and auto-seed fresh database on serverless cold starts
with app.app_context():
    try:
        db.create_all()
        from app.models import Product
        if Product.query.count() == 0:
            app.logger.info("Fresh database detected. Seeding KARTMART catalogue...")
            try:
                from seed_db import seed_database
                seed_database(app)
            except Exception as e_seed:
                app.logger.warning(f"seed_database warning: {e_seed}")

            try:
                from seed_catalog_expanded import seed_expanded_catalog
                seed_expanded_catalog(app)
            except Exception as e_exp:
                app.logger.warning(f"seed_expanded_catalog warning: {e_exp}")
    except Exception as e:
        app.logger.warning(f"Database initialization note: {e}")

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
