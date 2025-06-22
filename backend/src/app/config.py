import os

class Config:
    TESTING = False
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')


class ProductionConfig:
    pass


class DevelopmentConfig:
    SECRET_KEY ='dev'
    #SQLALCHEMY_DATABASE_URI ='sqlite:///diobank.sqlite'
    JWT_SECRET_KEY ='super-secret'


class TestingConfig:
    TESTING = True
    SECRET_KEY='test'
    #SQLALCHEMY_DATABASE_URI = "sqlite://"
    JWT_SECRET_KEY = 'test'