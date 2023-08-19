import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:zWHtLA4ywiKaUSLjSLPlo6mG2o4n62hq@dpg-cjg2seb6fquc73amcjs0-a.singapore-postgres.render.com/aigodb'


class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
