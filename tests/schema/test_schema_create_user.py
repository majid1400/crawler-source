import pytest

from app.schema.apiv1 import CreateUserRequest


def test_create_user_request_valid_data(data):
    request = CreateUserRequest(**data)
    assert request.country == "ir"
    assert request.sub_platform == "post"
    assert request.user_id == "1234568"
    assert request.user_name == "kamali"


def test_create_user_request_missing_data(data):
    request = CreateUserRequest(**data)
    with pytest.raises(AssertionError):
        assert request.country == 123
        assert request.sub_platform == 123
        assert request.user_id == 123
        assert request.user_name == 123


def test_create_user_request_missing_field():
    invalid_data = {"sub_platform": "post", "user_id": 1234568, "user_name": "kamali"}
    with pytest.raises(ValueError):
        CreateUserRequest(**invalid_data)
