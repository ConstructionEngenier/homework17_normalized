class Config(object):
    DEBUG = True
    SECRET = 'test'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./main.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
