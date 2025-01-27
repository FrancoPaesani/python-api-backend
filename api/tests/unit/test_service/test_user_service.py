import pytest
from unittest.mock import Mock
from domain.user import User
from schemas.management_schema import UserRequest
from services.user_service import UserService
from faker import Faker

fake = Faker()


@pytest.fixture
def mock_user_repository():
    return Mock()


@pytest.fixture
def mock_permission_repository():
    return Mock()


@pytest.fixture
def user_service(mock_user_repository, mock_permission_repository):
    return UserService(
        user_repository=mock_user_repository,
        permissions_repository=mock_permission_repository,
    )


def test_create_user_successfully(user_service, mock_user_repository):
    code = fake.name().upper().replace(" ", "")
    user_request = UserRequest(
        code=code,
        name=fake.name().upper(),
        email=fake.email(),
        hashed_password=fake.password(),
    )

    user_return_value = User(
        id=1,
        code=user_request.code,
        name=user_request.name,
        email=user_request.email,
        hashed_password=user_request.hashed_password,
        active=True,
    )

    mock_user_repository.get_user_by_code.return_value = None
    mock_user_repository.create_user.return_value = user_return_value

    created_user = user_service.create_user(user_request)

    assert created_user.code == user_request.code
    assert created_user.name == user_request.name
    assert created_user.email == user_request.email
    mock_user_repository.get_user_by_code.assert_called_once_with(code)
    mock_user_repository.create_user.assert_called_once()


def test_create_user_duplicate_code(user_service, mock_user_repository):
    duplicated_code = fake.name().upper().replace(" ", "")
    # Datos de entrada
    user_request = UserRequest(
        code=duplicated_code,
        name=fake.name().upper(),
        email=fake.email(),
        hashed_password=fake.password(),
    )

    mock_user_repository.get_user_by_code.return_value = User(
        code=duplicated_code,
        name=fake.name().upper(),
        email=fake.email(),
        hashed_password=fake.password(),
    )

    with pytest.raises(Exception, match="El código de usuario ingresado ya existe"):
        user_service.create_user(user_request)

    mock_user_repository.get_user_by_code.assert_called_once_with(duplicated_code)
    mock_user_repository.create_user.assert_not_called()


def test_enable_user(user_service, mock_user_repository):
    code = fake.name().upper().replace(" ", "")
    mock_user_repository.change_state.return_value = User(
        code=code,
        name=fake.name().upper(),
        email=fake.email(),
        hashed_password=fake.password(),
        active=True,
    )

    updated_user = user_service.enable_user(user_id=1)

    assert updated_user.active is True
    mock_user_repository.change_state.assert_called_once_with(1, True)


def test_disable_user(user_service, mock_user_repository):
    code = fake.name().upper().replace(" ", "")
    mock_user_repository.change_state.return_value = User(
        code=code,
        name=fake.name().upper(),
        email=fake.email(),
        hashed_password=fake.password(),
        active=False,
    )

    updated_user = user_service.disable_user(user_id=1)

    assert updated_user.active is False
    mock_user_repository.change_state.assert_called_once_with(1, False)
