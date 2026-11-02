import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'kartmart-secret-key-development-2026')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///kartmart.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Store Branding
    STORE_NAME = 'KARTMART'
    STORE_TAGLINE = 'India’s Favorite Modern Shopping Hub'
    CURRENCY_SYMBOL = '₹'
    
    # Default Demo Credentials
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@kartmart.local')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'Admin@123')
    ADMIN_REGISTRATION_KEY = os.getenv('ADMIN_REGISTRATION_KEY', 'Admin@2026')
    CUSTOMER_EMAIL = os.getenv('CUSTOMER_EMAIL', 'customer@kartmart.local')
    CUSTOMER_PASSWORD = os.getenv('CUSTOMER_PASSWORD', 'Customer@123')


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'


class TestingConfig(Config):
    TESTING = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'sqlite:///:memory:')


config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
