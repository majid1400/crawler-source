import pytest
from pymongo.cursor import Cursor
from pymongo.errors import WriteError
from pymongo.results import InsertOneResult, InsertManyResult


def test_insert(mongo, data):
    result = mongo.insert(data)
    assert "_id" in data
    assert isinstance(result, InsertOneResult) is True


def test_insert_many(mongo, data_collection):
    result = mongo.insert(data_collection)
    assert "_id" in data_collection[0]
    assert isinstance(result, InsertManyResult) is True


def test_insert_error(mongo, data):
    result = mongo.insert([data, data])
    assert "Error" in result


def test_find_all(mongo):
    result = mongo.find_all()
    assert isinstance(result, Cursor)
    assert '_id' in result[0]


def test_find_all_error(mongo):
    result = mongo.find_all('*')
    assert isinstance(result, dict)
    assert 'Error' in result
    assert result['Error'].split(',')[1] in ' bson.son.SON'


def test_find_one(mongo, data):
    result = mongo.find_one(data)
    assert '_id' in result
    assert result.get('user_name') in 'kamali'
    assert isinstance(result, dict)


def test_find_one_error(mongo, data):
    result = mongo.find_one(Exception)
    assert isinstance(result, dict)
    assert 'Error' in result
    assert result['Error'].split(',')[0] in "cannot encode object: <class 'Exception'>"


def test_update_mongo(mongo, data):
    old_value = data
    new_value = {"user_id": "40"}
    result_update = mongo.update(old_value, new_value)
    result = mongo.find_one(new_value)
    assert result_update is None
    assert result["user_id"] == "40"
    assert result["user_name"] == "kamali"


def test_update_mongo_error(mongo, data):
    old_value = data
    new_value = "ali"
    with pytest.raises(WriteError):
        mongo.update(old_value, new_value)


def test_mongo_delete_one(mongo, data):
    query = {"user_name": "kamali"}
    result_delete = mongo.delete_one(query)
    assert result_delete is None


def test_mongo_delete_one_error(mongo):
    result = mongo.delete_one('s')
    assert isinstance(result, dict)
    assert 'Error' in result
    assert result['Error'].split(',')[0] in "filter must be an instance of dict"


def test_mongo_delete_many(mongo, data_collection):
    result_delete = mongo.delete_many({"user_name": {"$regex": "^kamali"}})
    result = mongo.find_one({"user_name": "kamali"})
    assert result_delete is None
    assert result is None


def test_mongo_delete_error(mongo):
    result = mongo.delete_many('s')
    assert isinstance(result, dict)
    assert 'Error' in result
    assert result['Error'].split(',')[0] in "filter must be an instance of dict"
