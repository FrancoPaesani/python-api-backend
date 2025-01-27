from faker import Faker
from persistence.models.user_models import PermissionsDB
from persistence.repositories.permission_repository import PermissionRepository

fake = Faker()


def test_create_permission(db_session):
    repo = PermissionRepository(db_session)

    code, name = (
        fake.name().upper()[0:3],
        fake.text()[0:15],
    )

    new_permission = PermissionsDB(code=code, name=name)
    repo.create_permission(repo.to_domain(new_permission))
    permission_in_db = repo.get_permission_by_code(code)

    assert permission_in_db is not None
    assert permission_in_db.name == name
