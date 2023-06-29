def test_post_invalid_uri(client, data):
    response = client.post("platforms/telegram/user", json=data)
    assert response.status_code == 404
    assert response.json()['detail'] == 'Not Found'


def test_get_invalid_uri(client):
    response = client.get("/platforms/telegram/sources/invalid")
    assert response.status_code == 500
    assert response.json().get('code') == 102
    assert response.json().get(
        'Error') == "'invalid' is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string"


def test_get_user_id_with_error_message():
    # TODO : Implement update method
    pass
