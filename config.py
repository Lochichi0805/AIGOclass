import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgres://aigodb:1S2DFyAepcx5uAGNTZjeba5aFHoJk61M@dpg-cjbj1p7db61s7397arcg-a.singapore-postgres.render.com/mspa_4e9z'


class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
