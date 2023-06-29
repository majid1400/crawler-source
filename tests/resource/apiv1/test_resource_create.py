import pytest

from app.controller.apiv1 import UserController


@pytest.mark.parametrize(
    ("payload", "status", "code"),
    [
        ({"country": " ", "priority": 1, "sub_platform": "post", "user_id": "", "user_name": "", "link": ""}, 400, None),
        ({"country": "ir", "priority": 1, "sub_platform": "post", "user_id": " 123", "user_name": "", "link": ""}, 200, 100),
        ({"country": "ir", "priority": 1, "sub_platform": "post", "user_id": "", "user_name": "", "link": ""}, 400, None),
        ({"country": "ir", "priority": 1, "sub_platform": "post", "user_id": "12", "user_name": "", "link": ""}, 200, 100),
        ({"country": "ir", "priority": 1, "sub_platform": "post", "user_id": "12", "user_name": "", "link": ""}, 409, 117),
        ({"country": "ir", "priority": 1, "sub_platform": "post", "user_id": "12", "user_name": "kamali110", "link": ""}, 409, 117),
        ({"country": "ir", "priority": 1, "sub_platform": "post", "user_id": "", "user_name": "kamali110", "link": ""}, 200, 100),
        ({"country": "ir", "priority": 1, "sub_platform": "post", "user_id": "", "user_name": "kamali110", "link": ""}, 409, 117),
        ({"country": "ir", "priority": 1, "sub_platform": "post", "user_id": "", "user_name": "", "link": "xxdsafaef"}, 200, 100),
        ({"country": "ir", "priority": 1, "sub_platform": "post", "user_id": "", "user_name": "", "link": "xxdsafaef"}, 409, 117),
        ({"country": "ir", "priority": 1, "sub_platform": "post", "user_id": "12", "user_name": "kamali110", "link": "xxd"}, 409, 117),
        ({"country": "ir", "priority": 1, "sub_platform": "", "user_ids": "4578", "user_name": "", "link": ""}, 422, None),
        ({"country": "ir", "priority": 1, "sub_platform": "", "user_id": "4578", "user_name": "", "link": ""}, 422, None),
        ({"country": "", "priority": 1, "sub_platform": "post", "user_id": "4578", "user_name": "", "link": ""}, 422, None),
        ({"country": "", "priority": 1, "sub_platform": "post", "user_id": "4578", "user_name": "", "link": "",
          "test": "invalid_field"}, 422, None),
        ({"country": "", "priority": 1, "sub_platform": "", "user_id": "", "user_name": "", "link": ""}, 422, None),
        ({"country": "", "priority": 1, "sub_platform": "", "user_id": "", "user_name": ""}, 422, None),
        ({"country": "", "priority": 1, "sub_platform": "", "user_id": "12", "user_name": ""}, 422, None),
        ({}, 422, None),
    ]
)
def test_create_user_schema_require(uri, client, payload, status, code):
    response = client.post(uri, json=payload)

    assert response.status_code == status
    assert response.json().get('code') == code



@pytest.mark.parametrize(
    ("payload", "status", "code"),
    [
        ({"country": None, "priority": 1, "sub_platform": "post", "user_id": "test1", "user_name": "", "link": ""}, 422, None),
        ({"country": " ", "priority": 1, "sub_platform": "post", "user_id": "test1", "user_name": "", "link": ""}, 400, None),
        ({"country": " ir", "priority": 1, "sub_platform": "post", "user_id": "test1", "user_name": "", "link": ""}, 200, 100),
        ({"country": "ir", "priority": None, "sub_platform": "post", "user_id": "test1", "user_name": "", "link": ""}, 422, None),
        ({"country": "ir", "priority": 1, "sub_platform": None, "user_id": "test1", "user_name": "", "link": ""}, 422, None),
        ({"country": "ir", "priority": 1, "sub_platform": " ", "user_id": "test1", "user_name": "", "link": ""}, 400, None),
        ({"country": "ir", "priority": 1, "sub_platform": " post", "user_id": "test2", "user_name": "", "link": ""}, 200, 100),
        ({"country": "ir", "priority": 1, "sub_platform": "post", "user_id": None, "user_name": "", "link": ""}, 400, None),
        ({"country": "ir", "priority": 1, "sub_platform": "post", "user_id": " ", "user_name": "", "link": ""}, 400, None),
        ({"country": "ir", "priority": 1, "sub_platform": "post", "user_id": " test3", "user_name": "", "link": ""}, 200, 100),
        ({"country": "ir", "priority": 1, "sub_platform": "post", "user_id": "", "user_name": None, "link": ""}, 400, None),
        ({"country": "ir", "priority": 1, "sub_platform": "post", "user_id": "", "user_name": " ", "link": ""}, 400, None),
        ({"country": "ir", "priority": 1, "sub_platform": "post", "user_id": "", "user_name": " test1 ", "link": ""}, 200, 100),
        ({"country": "ir", "priority": 1, "sub_platform": "post", "user_id": "", "user_name": "", "link": None}, 400, None),
        ({"country": "ir", "priority": 1, "sub_platform": "post", "user_id": "", "user_name": "", "link": " "}, 400, None),
        ({"country": "ir", "priority": 1, "sub_platform": "post", "user_id": "", "user_name": "", "link": " test"}, 200, 100),
        ({"country": "ir", "priority": 1, "sub_platform": "post", "user_id": " test4 ", "user_name": " test3 ", "link": " test"}, 200, 100),
    ]
)
def test_create_user_space(uri, client, payload, status, code):
    response = client.post(uri, json=payload)

    assert response.status_code == status
    assert response.json().get('code') == code

    if response.status_code == 200:
        source_id = response.json().get('source_id')
        result = client.get(f"{uri}/{source_id}")
        assert result.json().get("sub_platform") == "post"
        assert result.json().get("country") == "ir"
        try:
            assert result.json().get("user_id") in ["test1", "test2", "test3", "test4"]
        except AssertionError:
            try:
                assert result.json().get("user_name") == "test1"
            except AssertionError:
                assert result.json().get("link") == "test"


@pytest.mark.parametrize(
    ("payload", "status", "code"),
    [
        ({"country": "ir", "priority": 1, "sub_platform": "post", "user_id": "1233", "user_name": "", "link": ""}, 200, 100),
        ({"country": "ir", "priority": 6, "sub_platform": "post", "user_id": "123", "user_name": "", "link": ""}, 422, None),
        ({"country": "ir", "priority": -1, "sub_platform": "post", "user_id": "123", "user_name": "", "link": ""}, 422, None),
        ({"country": "ir", "priority": "5", "sub_platform": "post", "user_id": "1234", "user_name": "", "link": ""}, 200, 100),
    ]
)
def test_create_user_priority(uri, client, payload, status, code):
    response = client.post(uri, json=payload)

    assert response.status_code == status
    assert response.json().get('code') == code


def test_create_user_controller_exception_server(uri, error_message_500, client, data, monkeypatch):
    def mock_create_user(platform=None, user=None):
        return {'Error': 'Internal server error'}

    monkeypatch.setattr(UserController, "get_user", mock_create_user)

    response = client.post(uri, json=data)

    assert response.status_code == 500
    assert response.json().get('code') == 102
    assert response.json().get('Error') == error_message_500


def test_create_user_controller_exception_existing_user(client, data, monkeypatch):
    def mock_create_user(platform=None, user=None):
        return data

    monkeypatch.setattr(UserController, "get_user", mock_create_user)

    response = client.post("/platforms/telegram/sources", json=data)

    assert response.status_code == 409
    assert response.json().get('code') == 117


def test_create_user_controller_exception_insert_user(error_message_500, client, data, monkeypatch):
    def mock_create_user(platform=None, user=None):
        return None

    monkeypatch.setattr(UserController, "get_user", mock_create_user)

    def mock_insert_user(data_test=None):
        return {"Error": error_message_500}

    monkeypatch.setattr(UserController.collection, "insert", mock_insert_user)

    response = client.post("/platforms/telegram/sources", json=data)

    assert response.status_code == 500
    assert response.json().get('code') == 102
    assert response.json().get('Error') == error_message_500
