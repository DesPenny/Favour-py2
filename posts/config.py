class DevelopmentConfig(object):
    DATABASE_URI = "postgresql://action:action@localhost:5432/posts"
    DEBUG = True
    UPLOAD_FOLDER = "uploads"
    
    IMAGES_PATH = ['uploads']
class TestingConfig(object):
    DATABASE_URI = "postgresql://action:action@localhost:5432/posts-test"
    DEBUG = True
    UPLOAD_FOLDER = "test-uploads"
    
