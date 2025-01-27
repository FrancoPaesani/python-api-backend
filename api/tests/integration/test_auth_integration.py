from faker import Faker

from persistence.models.user_models import UserDB

fake = Faker()


def create_credentials(code: str, hashed_password: str) -> dict:
    return {"code": code, "hashed_password": hashed_password}


def test_login_without_users_in_database(test_client):
    response = test_client.post(
        "/auth/login/",
        json=create_credentials(
            code=fake.name().upper().replace(" ", ""), hashed_password=fake.password()
        ),
    )

    assert response.status_code == 403


def test_create_user_then_login_without_permissions_successfully(
    test_client, db_session_client
):
    user_code = fake.name().upper().replace(" ", "")
    password = fake.password()

    user_db = UserDB(
        code=user_code, name=user_code, hashed_password=password, email=fake.email()
    )

    db_session_client.add(user_db)
    db_session_client.commit()
    db_session_client.refresh(user_db)

    response = test_client.post(
        "/auth/login/",
        json=create_credentials(code=user_code, hashed_password=password),
    )

    data = response.json()

    assert response.status_code == 200
    assert len(data["permissions"]) == 0


def test_logout_without_open_session(test_client):
    response = test_client.post("/auth/logout/")

    assert response.status_code == 403


def test_create_user_then_login_and_logout_successfully(test_client, db_session_client):
    user_code = fake.name().upper().replace(" ", "")
    password = fake.password()

    user_db = UserDB(
        code=user_code, name=user_code, hashed_password=password, email=fake.email()
    )

    db_session_client.add(user_db)
    db_session_client.commit()
    db_session_client.refresh(user_db)

    response = test_client.post(
        "/auth/login/",
        json=create_credentials(code=user_code, hashed_password=password),
    )
    data = response.json()

    assert response.status_code == 200
    assert len(data["permissions"]) == 0

    response = test_client.post("/auth/logout/")

    assert response.json() is True
