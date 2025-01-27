from domain.user import User
from faker import Faker

fake = Faker()


def test_create_user_successfully():
    name = name = fake.name().upper()

    user = User(
        code=fake.name().upper().replace(" ", ""),
        name=name,
        email=fake.email(),
        hashed_password=fake.name(),
    )

    assert user.name == name


def test_fail_to_create_user_invalid_email():
    name = fake.name().upper()
    try:
        user = User(
            code=fake.name().upper().replace(" ", ""),
            name=name,
            email="",
            hashed_password=fake.name(),
        )
        assert user.name == name
    except ValueError as e:
        assert type(e) is ValueError
