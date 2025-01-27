from domain.permission import Permission
from persistence.repositories.permission_repository import PermissionRepository
from utils.permissions_data import permissions_data
from persistence.database import session


def populate_permissions_table():
    db = session()
    permission_repository = PermissionRepository(db)
    for permission in permissions_data:
        permission_db = permission_repository.get_permission_by_code(permission["code"])
        if permission_db is None:
            permission_repository.create_permission(
                Permission(code=permission["code"], name=permission["name"])
            )
