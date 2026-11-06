import os
import sys

# Add project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db

app = create_app()

# Auto-create tables on serverless initialization if they don't exist
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        app.logger.warning(f"Database initialization note: {e}")

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
