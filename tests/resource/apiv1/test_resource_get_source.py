def test_get_sources_by_platform_susccess(client, data):
    data["user_id"] = "usertest_6"
    client.post("platforms/twitter/sources", json=data)

    data["user_id"] = "usertest_7"
    response = client.post("platforms/twitter/sources", json=data)

    assert response.status_code == 200

    response = client.get("platforms/twitter/sources")
    assert response.status_code == 200
    assert len(response.json()) == 2
