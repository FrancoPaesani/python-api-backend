def test_healthcheck_endpoint(test_client):
    response = test_client.get("/utils/healthcheck/")

    assert response.status_code == 200


def test_version_endpoint(test_client):
    response = test_client.get("/utils/version/")
    response_json = response.json()

    assert response.status_code == 200
    assert "version" in response_json
