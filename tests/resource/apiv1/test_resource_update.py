import pytest

from app.schema.apiv1 import UpdateUserRequest


@pytest.mark.parametrize(
    ("item", "status", "code"),
    [
        ({"country": "usa"}, 200, 100)
    ]
)
def test_update_user(client, uri, item, status, code):
    data = {"country": "ir", "priority": 1, "sub_platform": "post", "user_id": "usertest_8", "user_name": "kamali"}
    response_post = client.post("/platforms/telegram/sources", json=data)
    user_id = response_post.json().get('source_id')

    request = UpdateUserRequest(**item)
    response = client.put(f"{uri}/{user_id}", json=request.dict())

    assert response.status_code == status
    assert response.json().get('code') == code

    response_get = client.get(f"{uri}/{user_id}")
    assert "usa" == response_get.json().get('country')


@pytest.mark.parametrize(
    ("uri_test", "status", "code"),
    [
        ("/platforms/telegram/sources/invalid_user_id", 500, 102),
        ("/platforms/telegram/sources/6491416c31fb762cc93bc245", 404, 111),
    ]
)
def test_update_user_invalid(client, uri_test, status, code):
    request_data = {
        "country": "usa"
    }
    request = UpdateUserRequest(**request_data)
    response = client.put(uri_test, json=request.dict())

    assert response.status_code == status
    assert response.json().get('code') == code
