from persistence.repositories.permission_repository import PermissionRepository
from schemas.management_schema import UserRequest
from domain.user import User, UserWithPermissions
from persistence.repositories.user_repository import UserRepository


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
        permissions_repository: PermissionRepository,
    ):
        self.user_repository = user_repository
        self.permissions_repository = permissions_repository

    def create_user(self, user: UserRequest) -> User:
        new_user = User(
            code=user.code,
            name=user.name,
            email=user.email,
            hashed_password=user.hashed_password,
        )
        if self.user_repository.get_user_by_code(new_user.code) is not None:
            raise Exception("El código de usuario ingresado ya existe")
        return self.user_repository.create_user(new_user)

    def enable_user(self, user_id: int) -> User:
        return self.user_repository.change_state(user_id, True)

    def disable_user(self, user_id: int) -> User:
        return self.user_repository.change_state(user_id, False)

    def get_user_with_permissions_by_id(self, user_id: int) -> UserWithPermissions:
        user = self.user_repository.get_user_by_id(user_id)
        permissions = self.permissions_repository.get_user_permissions(user.id)

        user.permissions = permissions

        return user
