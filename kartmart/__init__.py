import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import config_by_name

# Initialize database instance
db = SQLAlchemy()


def create_app(config_name=None):
    """Application factory for KARTMART."""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
        
    config_class = config_by_name.get(config_name, config_by_name['default'])
    
    app = Flask(
        __name__,
        template_folder='../templates',
        static_folder='../static'
    )
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    from .routes import main_bp
    app.register_blueprint(main_bp)
    
    return app
