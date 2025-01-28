from sqlalchemy.orm import Session

from persistence.models.user_models import PermissionsDB, UserPermissionsDB
from domain.permission import Permission


class PermissionRepository:
    def __init__(self, db: Session):
        self.db = db

    @classmethod
    def from_domain(cls, permission: Permission) -> PermissionsDB:
        return PermissionsDB(
            id=permission.id, code=permission.code, name=permission.name
        )

    @classmethod
    def to_domain(cls, permission: PermissionsDB) -> Permission:
        return Permission(id=permission.id, code=permission.code, name=permission.name)

    def create_permission(self, permission: Permission) -> Permission:
        permission_db = PermissionRepository.from_domain(permission)

        self.db.add(permission_db)
        self.db.commit()
        self.db.refresh(permission_db)
        permission.id = permission_db.id

        return permission

    def get_permission_by_code(self, code: str) -> Permission | None:
        permission_db = (
            self.db.query(PermissionsDB).filter(PermissionsDB.code == code).first()
        )
        if permission_db is not None:
            return PermissionRepository.to_domain(permission_db)
        return None

    def get_all_permissions(self) -> list[Permission]:
        permissions_db = self.db.query(PermissionsDB).all()
        permissions_db = [PermissionRepository.to_domain(x) for x in permissions_db]

        return permissions_db

    def get_user_permissions(self, user_id: int) -> list[Permission]:
        permissions_db = (
            self.db.query(PermissionsDB)
            .join(UserPermissionsDB)
            .filter(UserPermissionsDB.user_id == user_id)
            .all()
        )

        user_permissions = list(
            map(
                lambda x: self.to_domain(x),
                permissions_db,
            )
        )

        return user_permissions
