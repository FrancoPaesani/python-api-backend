from faker import Faker
from persistence.repositories.permission_repository import PermissionRepository
from persistence.models.user_models import PermissionsDB, UserDB
from persistence.repositories.user_repository import UserRepository

fake = Faker()


def test_create_user(db_session):
    repo = UserRepository(db_session)

    code, name, email, hashed_password = (
        "AAA",
        fake.name(),
        fake.email(),
        fake.password(),
    )

    new_user = UserDB(
        code=code, name=name, email=email, hashed_password=hashed_password
    )
    repo.create_user(repo.user_to_domain(new_user))

    user_in_db = db_session.query(UserDB).filter_by(code=code).first()
    assert user_in_db is not None
    assert user_in_db.name == name


def test_create_user_then_change_state_to_false(db_session):
    repo = UserRepository(db_session)

    code, name, email, hashed_password = (
        "AAA",
        fake.name(),
        fake.email(),
        fake.password(),
    )

    new_user = UserDB(
        code=code, name=name, email=email, hashed_password=hashed_password
    )
    repo.create_user(repo.user_to_domain(new_user))

    user_in_db = db_session.query(UserDB).filter_by(code=code).first()
    assert user_in_db.name == name

    repo.change_state(user_in_db.id, False)

    user_in_db = repo.get_user_by_id(user_in_db.id)
    assert user_in_db.active is False


def test_create_user_without_permissions_then_get_permissions(db_session):
    repo = UserRepository(db_session)

    code, name, email, hashed_password = (
        "AAA",
        fake.name(),
        fake.email(),
        fake.password(),
    )

    new_user = UserDB(
        code=code, name=name, email=email, hashed_password=hashed_password
    )
    repo.create_user(repo.user_to_domain(new_user))

    user_in_db = db_session.query(UserDB).filter_by(code=code).first()
    assert user_in_db.name == name

    permissions = repo.get_permissions(user_in_db.id)

    assert len(permissions) == 0


def test_create_user_then_create_permission_and_assign_to_user(db_session):
    user_repo = UserRepository(db_session)

    code, name, email, hashed_password = (
        "AAA",
        fake.name(),
        fake.email(),
        fake.password(),
    )

    new_user = UserDB(
        code=code, name=name, email=email, hashed_password=hashed_password
    )
    new_user = user_repo.create_user(user_repo.user_to_domain(new_user))

    permission_repo = PermissionRepository(db_session)

    code, name = (
        fake.name().upper()[0:3],
        fake.name(),
    )

    while len(name) < 10:
        name = fake.name()

    new_permission = PermissionsDB(code=code, name=name)
    permission_repo.create_permission(new_permission)
    permission_in_db = permission_repo.get_permission_by_code(code)

    assert permission_in_db is not None
    assert permission_in_db.name == name

    user_repo.assign_permission(new_user.id, permission_in_db.id, new_user.id)

    user_permissions = user_repo.get_permissions(new_user.id)

    assert len(user_permissions) == 1
