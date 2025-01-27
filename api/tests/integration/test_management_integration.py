from faker import Faker


fake = Faker()


def create_user() -> dict:
    name = fake.name().upper()
    while len(name) < 10:
        name = fake.name().upper()
    return {
        "code": fake.name().upper().replace(" ", ""),
        "name": name,
        "email": fake.email(),
        "hashed_password": fake.password(),
    }


def create_permission() -> dict:
    name = fake.name().upper()
    while len(name) < 10:
        name = fake.name().upper()
    return {
        "code": fake.name().upper().replace(" ", "")[0:3],
        "name": name,
    }


def test_create_user(test_client, initialize_user_and_session):
    user_payload = create_user()

    response = test_client.post("/management/users/", json=user_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["code"] == user_payload["code"]
    assert data["name"] == user_payload["name"]
    assert data["email"] == user_payload["email"]


def test_create_permission(test_client, initialize_user_and_session):
    permission_payload = create_permission()

    response = test_client.post("/management/permissions/", json=permission_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == permission_payload["name"]


def test_assign_permission_to_user(test_client, initialize_user_and_session):
    user_payload = create_user()
    user_response = test_client.post("/management/users/", json=user_payload)
    user_id = user_response.json()["id"]

    permission_payload = create_permission()
    permission_response = test_client.post(
        "/management/permissions/", json=permission_payload
    )
    permission_id = permission_response.json()["id"]

    response = test_client.post(
        f"/management/users/permissions/?user_id={user_id}&permission_id={permission_id}"
    )

    assert response.status_code == 200
    data = response.json()

    assert data is True


def test_enable_user(test_client, initialize_user_and_session):
    user_payload = create_user()
    user_response = test_client.post("/management/users/", json=user_payload)
    user_id = user_response.json()["id"]

    response = test_client.post(f"/management/users/enable/?user_id={user_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["active"] is True


def test_disable_user(test_client, initialize_user_and_session):
    user_payload = create_user()
    user_response = test_client.post("/management/users/", json=user_payload)
    user_id = user_response.json()["id"]

    response = test_client.post(f"/management/users/disable/?user_id={user_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["active"] is False
