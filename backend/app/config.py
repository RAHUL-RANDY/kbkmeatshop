import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'fresh-meat-market-super-secret-key-2026')
    
    # MySQL Database Configuration
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_PORT = os.getenv('MYSQL_PORT', '3306')
    MYSQL_DB = os.getenv('MYSQL_DB', 'fresh_meat_market')

    # Construct MySQL Database URL
    DEFAULT_MYSQL_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4"
        if MYSQL_PASSWORD
        else f"mysql+pymysql://{MYSQL_USER}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4"
    )

    # Use explicit DATABASE_URL if given, else MySQL URI, or fallback SQLite
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', DEFAULT_MYSQL_URI)
    
    # Fallback indicator
    USE_SQLITE_FALLBACK = os.getenv('USE_SQLITE_FALLBACK', 'true').lower() in ('true', '1', 'yes')
    SQLITE_URI = f"sqlite:///{os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'fresh_meat_market.db'))}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }

    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-fresh-meat-market-secret-key-999')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=int(os.getenv('JWT_EXPIRE_DAYS', 7)))
    JWT_HEADER_TYPE = 'Bearer'

    # Razorpay Test Mode Credentials
    RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID', 'rzp_test_freshmeat2026')
    RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET', 'test_secret_freshmeat2026')

    # Default Seed Admin
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'kbkmeatshop@gmail.com')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'KBKMEAT12345678')
    ADMIN_NAME = os.getenv('ADMIN_NAME', 'Market Administrator')
    ADMIN_PHONE = os.getenv('ADMIN_PHONE', '9842729718')

    # Weekend Delivery Settings
    FREE_DELIVERY_THRESHOLD = 499.0
    STANDARD_DELIVERY_FEE = 49.0


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
