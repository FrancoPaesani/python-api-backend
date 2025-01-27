from persistence.repositories.user_repository import UserRepository
from domain.permission import Permission
from schemas.management_schema import PermissionRequest
from persistence.repositories.permission_repository import PermissionRepository


class ManagementService:
    def __init__(
        self,
        permission_repository: PermissionRepository,
        user_repository: UserRepository,
    ):
        self.user_repository = user_repository
        self.permission_repository = permission_repository

    def create_permission(self, permission: PermissionRequest) -> Permission:
        new_permission = Permission(code=permission.code, name=permission.name)

        if (
            self.permission_repository.get_permission_by_code(new_permission.code)
            is not None
        ):
            raise Exception("El código del permiso ya está en uso")
        new_permission = self.permission_repository.create_permission(new_permission)

        return new_permission

    def assign_permission(self, user_id: int, permission_id: int) -> bool:
        user_permissions = self.user_repository.get_permissions(user_id)
        user_permissions = list(map(lambda x: x.permission_id, user_permissions))

        if permission_id in user_permissions:
            raise Exception("El permiso ya se encuentra asignado al usuario")

        self.user_repository.assign_permission(user_id, permission_id)
        return True

    def get_all_permissions(self) -> list[Permission]:
        permissions = self.permission_repository.get_all_permissions()

        return permissions
