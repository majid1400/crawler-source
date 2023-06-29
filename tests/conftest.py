import pytest
from fastapi.testclient import TestClient

from app.config import Config
from app.main import app
from app.models.client import MongoDatabase
from app.models.database import MongoStorage

if 'test' not in Config.COLLECTION_NAME.split('_'):
    exit(0)


@pytest.fixture
def mongo():
    return MongoStorage(collection=Config.COLLECTION_NAME)


@pytest.fixture
def data():
    return {"country": "ir", "priority": 1, "sub_platform": "post", "user_id": "1234568", "user_name": "kamali"}


@pytest.fixture
def data_collection():
    return [
        {"country": "ir", "sub_platform": "post", "user_id": "1234568", "user_name": "kamali"},
        {"country": "rq", "sub_platform": "like", "user_id": "9874565", "user_name": "khadem"},
    ]


@pytest.fixture(scope="session", autouse=True)
def drop_test_collection():
    mongo = MongoDatabase()
    yield
    mongo.database[Config.COLLECTION_NAME].drop()


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def uri():
    return "platforms/telegram/sources"


@pytest.fixture
def error_message_500():
    return "Internal server error"


@pytest.fixture
def error_field_required():
    return "field required"
