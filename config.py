import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://m1016m:aynpduYUgaD2yAVFd8JLBgj2TPMPSWGD@dpg-cjbor97db61s73aeaou0-a.singapore-postgres.render.com/mspa_d63k'


class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
