class Config:

    SECRET_KEY = '\xfc\x03\x81\x7fW\x94"\x1a{,{\xa7'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):

    DEBUG = True
    MONGO_URI = 'mongodb://localhost:27017/python_test'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'ricardomussett@gmail.com'
    MAIL_PASSWORD = '3527354kbx'
    FLASKY_MAIL_SUBJECT_PREFIX = 'Alcaravan'
    FLASKY_MAIL_SENDER = 'ricardomussett@gmail.com'
    FLASKY_ADMIN = 'FLASKY_ADMIN'


class TestingConfig(Config):

    DEBUG = False
    MONGO_URI = 'mongodb://localhost:27017/python_test'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'ricardomussett@gmail.com'
    MAIL_PASSWORD = '3527354kbx'
    FLASKY_MAIL_SUBJECT_PREFIX = 'Alcaravan'
    FLASKY_MAIL_SENDER = 'ricardomussett@gmail.com'
    FLASKY_ADMIN = 'FLASKY_ADMIN'

class ProductionConfig(Config):

    DEBUG = False
    MONGO_URI = 'mongodb://localhost:27017/tableros' #por definir
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'ricardomussett@gmail.com' #por definir
    MAIL_PASSWORD = '3527354kbx' #por definir
    FLASKY_MAIL_SUBJECT_PREFIX = 'Alcaravan'
    FLASKY_MAIL_SENDER = 'ricardomussett@gmail.com' #por definir
    FLASKY_ADMIN = 'FLASKY_ADMIN'


config = {
    'development': DevelopmentConfig,
    'testing' : TestingConfig,
    'production' : ProductionConfig,
    'dafault' : DevelopmentConfig
}