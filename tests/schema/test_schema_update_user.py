from app.schema.apiv1 import UpdateUserRequest


def test_update_user_request():
    request_data = {
        "country": "USA",
        "sub_platform": "A",
        "user_name": "JohnDoe",
        "user_id": "123456"
    }
    request = UpdateUserRequest(**request_data)

    assert request.country == "USA"
    assert request.sub_platform == "A"
    assert request.user_name == "JohnDoe"
    assert request.user_id == "123456"
