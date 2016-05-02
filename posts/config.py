import os
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FAVOURSOUP_MAIL_SUBJECT_PREFIX = '[FavourSoup]'
    FAVOURSOUP_MAIL_SENDER = 'FavourSoup Admin <favoursoup@gmail.com>'
    FAVOURSOUP_ADMIN = os.environ.get('FavourSoup_ADMIN')

class DevelopmentConfig(object):
    DATABASE_URI = "postgresql://action:action@localhost:5432/posts"
    DEBUG = True
    UPLOAD_FOLDER = "uploads"
    
    IMAGES_PATH = ['uploads']
class TestingConfig(object):
    DATABASE_URI = "postgresql://action:action@localhost:5432/posts-test"
    DEBUG = True
    UPLOAD_FOLDER = "test-uploads"
    
