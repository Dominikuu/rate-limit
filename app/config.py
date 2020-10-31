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
    """
    Celery Config
    - CELERY_BROKER_URL uses `pyamqp`.
    - CELERY_IMPORTS registers tasks.
    - BROKER_HEARTBEAT of Celery App must be set to 0
        so that Rabbitmq will not disconnect the connection.
    """
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')
    CELERY_IMPORTS = ('app.tasks')
    CELERY_BROKER_HEARTBEAT = 0


class Production:
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
