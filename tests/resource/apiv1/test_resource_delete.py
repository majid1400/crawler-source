import pytest
from bson import ObjectId

from app.models.database import MongoStorage


def test_inactive_user(client, data):
    data["user_id"] = "as12345"
    response_post = client.post("/platforms/telegram/sources", json=data)
    user_id = response_post.json().get('source_id')
    response = client.delete(f"/platforms/telegram/sources/{user_id}")

    assert response.status_code == 200
    assert response.json().get('code') == 100
    assert response.json().get('status') == "success inactive user"

    collection = MongoStorage("inactive_users")
    result = collection.find_one({"_id": ObjectId(user_id), "platform": "telegram"})
    assert str(result.get('_id')) == user_id

    collection.delete_one({"_id": ObjectId(user_id), "platform": "telegram"})


@pytest.mark.parametrize(
    ("uri_test", "status", "code"),
    [
        ("/platforms/telegram/sources/invalid_user_id", 500, 102)
    ]
)
def test_inactive_user_invalid_data(client, uri_test, status, code):
    response = client.delete(uri_test)

    assert response.status_code == status
    assert response.json().get('code') == code
