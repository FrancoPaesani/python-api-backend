import random
from faker import Faker

from domain.action import Action

fake = Faker()


def test_create_action_successfully():
    description = fake.name()
    while len(description) <= 3:
        description = fake.name()

    action = Action(id=random.randint(1, 10), description=description)

    assert action.description == description


def test_fail_to_create_action_invalid_description():
    description = fake.name()[0:3]

    try:
        Action(id=random.randint(1, 10), description=description)
    except Exception as e:
        assert type(e) is ValueError
