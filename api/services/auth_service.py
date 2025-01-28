from datetime import datetime, timedelta

from domain.permission import Permission
from utils.auth_utils import create_jwt_token
from persistence.repositories.permission_repository import PermissionRepository
from domain.user import UserSession, UserWithPermissions
from persistence.repositories.user_repository import UserRepository
from schemas.management_schema import LoginUserRequest


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        permissions_repository: PermissionRepository,
    ):
        self.user_repository = user_repository
        self.permissions_repository = permissions_repository

    def create_user_session(
        self, user_id: int, permissions: list[Permission]
    ) -> UserSession:
        permissions_dict: list[dict] = list(
            map(lambda x: x.__dict__, permissions or [])
        )

        expiry_date = datetime.now() + timedelta(hours=2)
        jwt_token = create_jwt_token(
            {
                "user_id": user_id,
                "expiry_date": expiry_date,
                "permissions": permissions_dict,
            }
        )

        user_session = UserSession(
            user_id=user_id,
            jwt_token=str(jwt_token),
            expiry_date=datetime.now() + timedelta(hours=2),
        )

        user_session = self.user_repository.create_user_session(user_session)

        return user_session

    def authenticate_user(self, credentials: LoginUserRequest) -> UserWithPermissions:
        user = self.user_repository.get_user_by_code(user_code=credentials.code)

        if user is None or user.id is None:
            raise ConnectionRefusedError("Usuario inválido.")

        if user.hashed_password != credentials.hashed_password:
            raise ConnectionRefusedError("Usuario inválido.")

        permissions = self.permissions_repository.get_user_permissions(user.id)
        user_session = self.create_user_session(user.id, permissions)

        user = UserWithPermissions(**user.__dict__)

        user.permissions = permissions
        user.jwt_token = user_session.jwt_token

        return user

    def get_user_session(self, jwt_token: str) -> UserSession | None:
        return self.user_repository.get_user_session_by_token(jwt_token)

    def logout_user(self, user_id: int) -> bool:
        user_session = self.user_repository.get_user_session_by_id(user_id)

        if user_session is None:
            raise ConnectionRefusedError("Sesión inválida.")

        deleted = self.user_repository.delete_user_session(user_session)

        return deleted
