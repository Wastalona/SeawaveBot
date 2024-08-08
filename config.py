import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()

class Config:
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    

class DevelopmentConfig(Config):
    pass


class TestingConfig(Config):
    pass


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}