import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Development:
    """
    Development environment configuration
    """
    DEBUG = True
    TESTING = False
    TEMPLATES_AUTO_RELOAD = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = False
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.getenv('POSTGRES_URI')
    OPENAPI_VERSION = os.environ.get('OPENAPI_VERSION', '3.0.2')

class Production(object):
    """
    Production environment configurations
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

app_config = {
    'dev': 'Development',
    'prod': 'Production',
}