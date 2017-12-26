import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'ASKLJDask5djaksdjl3asd1'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class JobConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:266661@localhost/flask'


class HomeConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:266661@localhost/flask'


class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:266661@localhost/flask'


config = {
    'job': JobConfig,
    'home': HomeConfig,
    'prod': ProdConfig,

    'default': HomeConfig
}
