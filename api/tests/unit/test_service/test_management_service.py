import pytest
from unittest.mock import Mock
from faker import Faker
from domain.permission import Permission
from schemas.management_schema import PermissionRequest
from services.management_service import ManagementService

fake = Faker()


@pytest.fixture
def mock_permission_repository():
    return Mock()


@pytest.fixture
def mock_user_repository():
    return Mock()


@pytest.fixture
def management_service(mock_permission_repository, mock_user_repository):
    return ManagementService(
        permission_repository=mock_permission_repository,
        user_repository=mock_user_repository,
    )


def test_create_permission_success(management_service, mock_permission_repository):
    name = fake.text().capitalize()
    while len(name) < 10:
        name = fake.text().capitalize()
    permission_request = PermissionRequest(
        code=fake.text().upper()[0:3],
        name=name,
    )
    permission = Permission(
        code=permission_request.code, name=permission_request.name, id=fake.uuid4()
    )

    mock_permission_repository.get_permission_by_code.return_value = None
    mock_permission_repository.create_permission.return_value = permission

    created_permission = management_service.create_permission(permission_request)

    assert created_permission.code == permission_request.code
    assert created_permission.name == permission_request.name
    mock_permission_repository.get_permission_by_code.assert_called_once_with(
        permission_request.code
    )
    mock_permission_repository.create_permission.assert_called_once()


def test_create_permission_duplicate_code(
    management_service, mock_permission_repository
):
    name = fake.text().capitalize()
    while len(name) < 10:
        name = fake.text().capitalize()
    permission_request = PermissionRequest(
        code=fake.text().upper()[0:3],
        name=name,
    )

    mock_permission_repository.get_permission_by_code.return_value = Permission(
        **permission_request.dict()
    )

    with pytest.raises(Exception, match="El código del permiso ya está en uso"):
        management_service.create_permission(permission_request)

    mock_permission_repository.get_permission_by_code.assert_called_once_with(
        permission_request.code
    )


def test_assign_permission_success(management_service, mock_user_repository):
    user_id = fake.random_int(min=1, max=1000)
    permission_id = fake.random_int(min=1, max=100)
    user_permissions = []

    mock_user_repository.get_permissions.return_value = user_permissions
    mock_user_repository.assign_permission.return_value = True

    result = management_service.assign_permission(user_id, permission_id, user_id)

    assert result is True
    mock_user_repository.get_permissions.assert_called_once_with(user_id)
    mock_user_repository.assign_permission.assert_called_once_with(
        user_id, permission_id, user_id
    )


def test_assign_permission_duplicate(management_service, mock_user_repository):
    user_id = fake.random_int(min=1, max=1000)
    permission_id = fake.random_int(min=1, max=100)
    user_permissions = [Mock(permission_id=permission_id)]

    mock_user_repository.get_permissions.return_value = user_permissions

    with pytest.raises(
        Exception, match="El permiso ya se encuentra asignado al usuario"
    ):
        management_service.assign_permission(user_id, permission_id, user_id)

    mock_user_repository.get_permissions.assert_called_once_with(user_id)
    mock_user_repository.assign_permission.assert_not_called()
