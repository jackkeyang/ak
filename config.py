class Config:
    SECRET_KEY = '0LAFvVAbcufUX1SVNSaRBCp2PgIqVVz4'

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/ak?charset=utf8'

class ProductionConfig(Config):
    pass

config = {
    'dev': DevelopmentConfig,
    'pro': ProductionConfig,
    'default': DevelopmentConfig
}