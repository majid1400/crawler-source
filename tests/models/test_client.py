from app.models.client import MongoDatabase


def test_mongo_database_instance():
    db1 = MongoDatabase()
    db2 = MongoDatabase()
    assert db1 is db2
