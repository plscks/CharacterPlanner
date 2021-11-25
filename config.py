from os import environ, path
from dotenv import load_dotenv
import redis


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.cfg'))

class Config(object):
    DEBUG = True
    DEVELOPMENT = True
    FLASK_SECRET = environ.get('SECRET_KEY').encode('utf8')
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_TYPE = environ.get('SESSION_TYPE')
    SESSION_PERMANENT = environ.get('SESSION_PERMANENT')
    SESSION_REDIS = redis.from_url(environ.get('SESSION_REDIS'))

class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
