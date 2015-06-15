class DevelopmentConfig(object):
    DATABASE_URI = "postgresql://action:action@localhost:5432/posts"
    DEBUG = True
    UPLOAD_FOLDER = "uploads"
    ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'bmp'])

class TestingConfig(object):
    DATABASE_URI = "postgresql://action:action@localhost:5432/posts-test"
    DEBUG = True
    UPLOAD_FOLDER = "test-uploads"
    ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'bmp'])
