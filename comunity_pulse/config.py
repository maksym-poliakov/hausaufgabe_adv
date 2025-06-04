class Config:

    DEBUG = False

    TESTING = False

    SQLALCHEMY_DATABASE_URI = "postgresql://postgres@localhost:5432/mybase_comunity_pulse"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):

    pass


class DevelopmentConfig(Config):

    DEBUG = True


class TestingConfig(Config):

    TESTING = True


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig,
    default=DevelopmentConfig,
)
