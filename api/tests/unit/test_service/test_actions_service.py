import pytest
from unittest.mock import Mock
from faker import Faker
from schemas.action_schema import ActionRequest, ActionResponse
from services.actions_service import ActionService

fake = Faker()


@pytest.fixture
def mock_action_repository():
    return Mock()


@pytest.fixture
def action_service(mock_action_repository):
    return ActionService(action_repository=mock_action_repository)


def test_create_action_success(action_service, mock_action_repository):
    action_request = ActionRequest(description=fake.sentence(nb_words=5))

    mock_action_repository.create_action.return_value = ActionResponse(
        id=fake.random_int(min=1, max=1000),
        description=action_request.description,
    )

    created_action = action_service.create_action(action_request)

    assert created_action.description == action_request.description
    mock_action_repository.create_action.assert_called_once()


def test_get_actions(action_service, mock_action_repository):
    actions = [
        ActionResponse(
            id=fake.random_int(min=1, max=1000), description=fake.sentence(nb_words=5)
        )
        for _ in range(3)
    ]

    mock_action_repository.get_actions.return_value = actions

    retrieved_actions = action_service.get_actions()

    assert len(retrieved_actions) == 3
    mock_action_repository.get_actions.assert_called_once()
