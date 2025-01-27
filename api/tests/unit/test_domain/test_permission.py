from faker import Faker

from domain.permission import Permission

fake = Faker()


def test_create_permission_successfully():
    name = fake.name()
    while len(name) < 10:
        name = fake.name()

    permission = Permission(code=fake.text()[0:3], name=name)

    assert permission.name == name


def test_fail_to_create_permission_invalid_name():
    name = fake.name()[0:5]

    try:
        Permission(code=fake.text()[0:3], name=name)
    except Exception as e:
        assert type(e) is ValueError


def test_fail_to_create_permission_invalid_code():
    name = fake.name()
    while len(name) < 10:
        name = fake.name()

    try:
        Permission(code=fake.text()[0:2], name=name)
    except Exception as e:
        assert type(e) is ValueError
