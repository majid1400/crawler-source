from typing import Union

from app.models.client import MongoDatabase


class MongoStorage:
    def __init__(self, collection):
        self.mongo = MongoDatabase()
        self.collection = collection

    def insert(self, data: Union[dict, list]):
        collection = getattr(self.mongo.database, self.collection)
        try:
            if isinstance(data, list) and len(data) > 1:
                return collection.insert_many(data)
            else:
                return collection.insert_one(data)
        except Exception as e:
            return {"Error": str(e)}

    def find_all(self, query: dict = None):
        try:
            return self.mongo.database[self.collection].find(query)
        except Exception as e:
            return {"Error": str(e)}

    def find_one(self, query: dict = None):
        try:
            return self.mongo.database[self.collection].find_one(query)
        except Exception as e:
            return {"Error": str(e)}

    def delete_one(self, query: dict):
        collection = getattr(self.mongo.database, self.collection)
        try:
            collection.delete_one(query)
        except Exception as e:
            return {"Error": str(e)}

    def delete_many(self, query: dict):
        collection = getattr(self.mongo.database, self.collection)
        try:
            collection.delete_many(query)
        except Exception as e:
            return {"Error": str(e)}

    def update(self, old_value: dict, new_value: dict):
        collection = getattr(self.mongo.database, self.collection)
        collection.update_one(old_value, {"$set": new_value})
