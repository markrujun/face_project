import os
import json


basedir = os.path.abspath(os.path.dirname(__file__))
app_config_file = "appconfig.json"

with open(app_config_file, 'r') as f:
    data = json.load(f)
    f.close()
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '123.0asdx563c41.0y$%&1234'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASK_ADMIN = os.environ.get('FLASK_ADMIN')
    JSON_AS_ASCII = False
    HOST = "".join(data["HOST"])
    PHOTO_LENGTH  =  data["PHOTO_LENGTH"]
    PHOTO_WIDTH  =  data["PHOTO_WIDTH"]
    PHOTO_FORMAT  =  "".join(data["PHOTO_FORMAT"])
    PHOTO_DIR  =  "".join(data["PHOTO_DIR"])
    CONFIDENCE  =  data["CONFIDENCE"]

    

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'mysql+mysqlconnector://root:marujun123!@localhost/face'
    def __init__(self):
        with open(app_config_file, 'r') as f:
            data = json.load(f)
            print(data)

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'mysql+mysqlconnector://root:rootlocalhost@localhost/face'
    def __init__(self):
        with open(app_config_file, 'r') as f:
            data = json.load(f)
            print(data)

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}