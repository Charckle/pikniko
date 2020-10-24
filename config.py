import sys
from os import environ 

DB_HOST = environ.get('DB_HOST', "127.0.0.1")
DB_NAME = environ.get('DB_NAME', "svetovidprequel")
DB_USERNAME = environ.get('DB_USERNAME', "root")
DB_PASSWORD = environ.get('DB_PASSWORD', "")


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = environ.get('SECRET_KEY', "B\xb2?.\xdf\x9f\xa7m\xf8\x8a%,\xf7\xc4\xfa\x91")

    IMAGE_UPLOADS = "/home/username/app/app/static/images/uploads"

    SESSION_COOKIE_SECURE = True

    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2
    
    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED     = True
    
class ProductionConfig(Config):
    DB_HOST = DB_HOST
    DB_NAME = DB_NAME
    DB_USERNAME = DB_USERNAME
    DB_PASSWORD = DB_PASSWORD 

class DevelopmentConfig(Config):
    DEBUG = True

    DB_HOST = DB_HOST
    DB_NAME = DB_NAME
    DB_USERNAME = DB_USERNAME
    DB_PASSWORD = DB_PASSWORD

    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    TESTING = True

    DB_HOST = DB_HOST
    DB_NAME = DB_NAME
    DB_USERNAME = DB_USERNAME
    DB_PASSWORD = DB_PASSWORD

    SESSION_COOKIE_SECURE = False