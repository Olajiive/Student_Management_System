from decouple import config
import os
from datetime import timedelta

BASE_DIR= os.path.dirname(os.path.realpath(__file__))

class Config:
    SECRET_KEY = config('SECRET_KEY', "secret")
    JWT_ACCESS_TOKEN_EXPIRES =timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES =timedelta(minutes=30)
    JWT_SECRET_KEY= config("JWT_SECRET_KEY")

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS= False
    SQLALCHEMY_DATABASE_URI= "sqlite:///" + os.path.join(BASE_DIR, "db.sqlite")
    SQLALCHEMY_ECHO = True
    
class TestConfig(Config):
    TESTING= True
    SQLALCHEMY_TRACK_MODIFICATIONS= False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "sqlite://test.db"


class ProdConfig(Config):
    pass


config_dict = {
    "devconfig": DevConfig,
    "testconfig": TestConfig,
    "prodconfig":ProdConfig

}