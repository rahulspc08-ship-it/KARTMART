import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env
load_dotenv(BASE_DIR / '.env')


class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'kartmart-dev-default-secret-key-321')
    
    # Database URL from environment
    # Supports MySQL: mysql+pymysql://<user>:<password>@<host>:<port>/<db_name>
    # Defaults to SQLite if not explicitly provided
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///kartmart.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Store Configuration
    STORE_NAME = 'KARTMART'
    STORE_TAGLINE = 'Next-Gen E-Commerce Shopping Experience'


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    ENV = 'development'


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'sqlite:///:memory:')


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False


config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
