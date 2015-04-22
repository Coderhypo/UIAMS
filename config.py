SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost/comdb'
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    UPLOAD_FOLDER = '/app/uploads'
    SECRET_KEY = 'you-will-never-guess'
    FLASK_POSTS_PER_PAGE = 10

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost/dev_db'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost/comdb'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost/comdb'

config = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,
    'default':DevelopmentConfig
}
