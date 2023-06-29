import pytest
from bson import ObjectId


def test_get_sucsses_id(uri, data, client):
    data["user_id"] = "usertest_1"
    response_post = client.post(f"{uri}", json=data)
    user_id = response_post.json().get('source_id')
    response = client.get(f"{uri}/{user_id}")

    time = ObjectId(user_id).generation_time.replace(tzinfo=None).isoformat()

    assert response.status_code == 200
    assert response.json()['code'] == 100
    assert response.json() == {'country': 'ir', "priority": 1, 'platform': 'telegram', 'sub_platform': 'post', 'user_id': 'usertest_1',
                               'user_name': 'kamali', 'link': None, 'bio': None, 'member_count': None,
                               'follower_count': None, 'following_count': None, 'fetch_ts': None, 'create_time': time,
                               'status': 'pending', 'error_message': None, 'code': 100}


@pytest.mark.parametrize(
    ("user_id_test", "uri_test", "status", "code"),
    [
        ("usertest_4", "/platforms/telegram/sources", 200, 100),
        ("usertest_2", "/platforms/telegram/invalid", 404, None),
        ("usertest_3", "/platforms/instagram/sources", 422, 104),
        ("usertest_4", "/platforms/telegram/sources", 500, 102),
    ]
)
def test_get_invalid(client, uri, data, user_id_test, uri_test, status, code):
    data["user_id"] = user_id_test
    response_post = client.post(uri, json=data)

    user_id = response_post.json().get('source_id')
    response = client.get(f"{uri_test}/{user_id}")

    assert response.status_code == status
    assert response.json().get('code') == code


@pytest.mark.parametrize(
    ("user_id", "status", "code"),
    [
        ("0491416c31f5762cc93bc245", 422, 104),
        ("6491416c31f5762cc93bc245777777", 500, 102),
        ("6491", 500, 102)
    ]
)
def test_get_userid_not_found(client, uri, user_id, status, code):
    response = client.get(f"{uri}/{user_id}")

    assert response.status_code == status
    assert response.json().get('code') == code
