import os
from dotenv import load_dotenv

# dotenv_path = os.path.join(os.getcwd(), '.env')
load_dotenv()


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', default='')
    SECRET_KEY = os.environ.get('SECRET_KEY', default='')
    SECURITY_PASSWORD_SALT = os.environ.get(
        'SECURITY_PASSWORD_SALT', default='')

    MAIL_DEFAULT_SENDER = 'survey@mybqualityscansafecaregh.com'
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    SERVER_NAME = 'localhost:1122'

    UPLOAD_FOLDER = 'src/images'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:admin@localhost/flask_db'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:admin@localhost/library'
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_ECHO = False
