from faker import Faker
import pytest
from fastapi.testclient import TestClient
from persistence.repositories.user_repository import UserRepository
from services.management_service import ManagementService
from domain.permission import Permission
from persistence.repositories.permission_repository import PermissionRepository
from utils.permissions_data import permissions_data
from domain.user import UserWithPermissions
from persistence.models.user_models import UserDB
from tests.integration.test_auth_integration import create_credentials
from main_router import app
from persistence.database import Base, get_db
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker, Session

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session_client():
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def test_client(db_session_client):
    def get_session_override():
        return db_session_client

    app.dependency_overrides[get_db] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


fake = Faker()


@pytest.fixture
def create_user(db_session_client):
    user_code = fake.name().upper().replace(" ", "")
    password = fake.password()

    user_db = UserDB(
        code=user_code, name=user_code, hashed_password=password, email=fake.email()
    )

    db_session_client.add(user_db)
    db_session_client.commit()
    db_session_client.refresh(user_db)
    yield user_db


@pytest.fixture(autouse=True)
def populate_permissions(db_session_client):
    db = db_session_client
    permission_repository = PermissionRepository(db)
    for permission in permissions_data:
        permission_db = permission_repository.get_permission_by_code(permission["code"])
        if permission_db is None:
            permission_repository.create_permission(
                Permission(code=permission["code"], name=permission["name"])
            )


@pytest.fixture
def create_user_and_assign_all_permissions(create_user, db_session_client):
    user_id = create_user.id
    management_service = ManagementService(
        permission_repository=PermissionRepository(db_session_client),
        user_repository=UserRepository(db_session_client),
    )

    permissions = management_service.get_all_permissions()

    for x in permissions:
        management_service.assign_permission(user_id, x.id)

    yield create_user


@pytest.fixture
def initialize_user_and_session(test_client, create_user_and_assign_all_permissions):
    user_code = create_user_and_assign_all_permissions.code
    user_password = create_user_and_assign_all_permissions.hashed_password

    response = test_client.post(
        "/auth/login/",
        json=create_credentials(code=user_code, hashed_password=user_password),
    )

    yield UserWithPermissions(**response.json())
