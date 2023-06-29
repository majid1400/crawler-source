from pymongo import MongoClient

from app.config.config import Config


class MongoDatabase:
    instance = None

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(*args, **kwargs)
        return cls.instance

    def __init__(self):
        self.client = MongoClient(self.is_debug())
        self.database = self.client[Config.TABLE_NAME]

    @staticmethod
    def is_debug():
        if Config.USER_NAME is None or Config.PASSWORD is None:
            return f"mongodb://{Config.HOST}:{Config.PORT}/"
        else:
            return f"mongodb://{Config.USER_NAME}:{Config.PASSWORD}@{Config.HOST}:{Config.PORT}/" \
                   f"?authSource={Config.TABLE_NAME}&authMechanism=SCRAM-SHA-256"
