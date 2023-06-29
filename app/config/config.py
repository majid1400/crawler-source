from os import environ

from dotenv import load_dotenv

load_dotenv()


class Config:
    ######################### Application Config ########################################
    DEBUG = bool(int(environ.get("CONFIG_DEBUG", "0")))
    ENV = environ.get("CONFIG_ENV", "production")
    ######################### mongo Application Config ##################################
    USER_NAME = environ.get('CONFIG_MONGO_USER_NAME', None)
    PASSWORD = environ.get('CONFIG_MONGO_PASSWORD', None)
    TABLE_NAME = environ.get('CONFIG_MONGO_TABLE_NAME', 'crawler')
    COLLECTION_NAME = environ.get('CONFIG_MONGO_COLLECTION_NAME', None)
    HOST = environ.get('CONFIG_MONGO_HOST', 'localhost')
    PORT = int(environ.get('CONFIG_MONGO_PORT', 27017))
