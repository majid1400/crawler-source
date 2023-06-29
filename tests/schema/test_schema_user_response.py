import pytest

from app.schema.apiv1 import UserResponse, UserIdResponse

data_rsponse = {
    "country": "ir",
    "priority": 1,
    "platform": "telegram",
    "sub_platform": "post",
    "user_id": "1234568",
    "user_name": "kamali",
    "bio": "I love you",
    "member_count": 10,
    "follower_count": 125,
    "following_count": 1256,
    "fetch_ts": 1234564,
    "create_time": "2023-06-24T15:15:58",
    "status": "Pending",
}


def test_user_id_response_valid_data():
    request = UserIdResponse(**{"user_id": "648fe0c118df238c0cec7a35"})
    assert request.user_id == "648fe0c118df238c0cec7a35"


def test_user_response_invalid_data():
    request = UserResponse(**data_rsponse)
    assert request.country == "ir"
    assert request.priority == 1
    assert request.platform == "telegram"
    assert request.sub_platform == "post"
    assert request.user_id == "1234568"
    assert request.user_name == "kamali"
    assert request.bio == "I love you"
    assert request.member_count == 10
    assert request.follower_count == 125
    assert request.following_count == 1256
    assert request.fetch_ts == 1234564
    assert request.create_time == "2023-06-24T15:15:58"
    assert request.status == "Pending"
    assert request.error_message is None


def test_user_response_valid_data():
    data_rsponse["error_message"] = "Not Authorized"
    request = UserResponse(**data_rsponse)
    assert request.country == "ir"
    assert request.priority == 1
    assert request.platform == "telegram"
    assert request.sub_platform == "post"
    assert request.user_id == "1234568"
    assert request.user_name == "kamali"
    assert request.bio == "I love you"
    assert request.member_count == 10
    assert request.follower_count == 125
    assert request.following_count == 1256
    assert request.fetch_ts == 1234564
    assert request.create_time == "2023-06-24T15:15:58"
    assert request.status == "Pending"
    assert request.error_message == "Not Authorized"


def test_user_response_request_missing_field():
    invalid_data = {"sub_platform": "post", "user_id": 1234568, "user_name": "kamali"}
    with pytest.raises(ValueError):
        UserResponse(**invalid_data)
