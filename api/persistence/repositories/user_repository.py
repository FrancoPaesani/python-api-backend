from sqlalchemy.orm import Session

from persistence.models.auth_models import UserSessionDB
from domain.user import User, UserPermission, UserSession
from persistence.models.user_models import UserDB, UserPermissionsDB


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    @classmethod
    def user_from_domain(cls, user: User) -> UserDB:
        return UserDB(
            id=user.id,
            name=user.name,
            code=user.code,
            email=user.email,
            hashed_password=user.hashed_password,
            active=user.active,
        )

    @classmethod
    def user_to_domain(cls, user: UserDB) -> User:
        return User(
            id=user.id,
            name=user.name,
            code=user.code,
            email=user.email,
            hashed_password=user.hashed_password,
            active=user.active,
        )

    @classmethod
    def user_permission_from_domain(
        cls, user_permission: UserPermission
    ) -> UserPermissionsDB:
        return UserPermissionsDB(
            user_id=user_permission.user_id,
            permission_id=user_permission.permission_id,
            date_created=user_permission.date_created,
            user_created=user_permission.user_created,
        )

    @classmethod
    def user_permission_to_domain(
        cls, user_permission: UserPermissionsDB
    ) -> UserPermission:
        return UserPermission(
            user_id=user_permission.user_id,
            permission_id=user_permission.permission_id,
            date_created=user_permission.date_created,
            user_created=user_permission.user_created,
        )

    @classmethod
    def user_session_from_domain(cls, user_session: UserSession) -> UserSessionDB:
        return UserSessionDB(
            user_id=user_session.user_id,
            jwt_token=user_session.jwt_token,
            expiry_date=user_session.expiry_date,
            created=user_session.created,
        )

    @classmethod
    def user_session_to_domain(cls, user_session: UserSessionDB) -> UserSession:
        return UserSession(
            user_id=user_session.user_id,
            jwt_token=user_session.jwt_token,
            expiry_date=user_session.expiry_date,
            created=user_session.created,
        )

    def create_user(self, user: User) -> User:
        user_db = UserRepository.user_from_domain(user)

        self.db.add(user_db)
        self.db.commit()
        self.db.refresh(user_db)

        user.id = user_db.id
        user.active = user_db.active

        return user

    def change_state(self, user_id: int, new_state: bool) -> User:
        user_db = self.db.query(UserDB).get(user_id)

        user_db.active = new_state

        self.db.commit()
        self.db.refresh(user_db)

        return UserRepository.user_to_domain(user_db)

    def get_user_by_id(self, user_id: int) -> User | None:
        user_db = self.db.query(UserDB).get(user_id)

        if user_db is not None:
            return UserRepository.user_to_domain(user_db)
        return None

    def get_user_by_code(self, user_code: str) -> User | None:
        user_db = self.db.query(UserDB).filter(UserDB.code == user_code).first()

        if user_db is not None:
            return UserRepository.user_to_domain(user_db)

        return None

    def assign_permission(self, user_id: int, permission_id: int):
        user_permission_db = UserPermissionsDB(
            user_id=user_id, permission_id=permission_id
        )

        self.db.add(user_permission_db)
        self.db.commit()
        self.db.refresh(user_permission_db)

        return UserRepository.user_permission_to_domain(user_permission_db)

    def get_permissions(self, user_id: int) -> list[UserPermission]:
        user_permissions_db = (
            self.db.query(UserPermissionsDB)
            .filter(UserPermissionsDB.user_id == user_id)
            .all()
        )

        user_permissions = list(
            map(
                lambda x: UserRepository.user_permission_to_domain(x),
                user_permissions_db,
            )
        )

        return user_permissions

    def delete_user_session(self, user_session: UserSession) -> bool:
        user_session_db: UserSessionDB = self.db.query(UserSessionDB).get(
            user_session.user_id
        )
        self.db.delete(user_session_db)
        self.db.commit()

        return True

    def create_user_session(self, user_session: UserSession) -> UserSession:
        last_session = self.get_user_session_by_id(user_session.user_id)

        if last_session is not None:
            self.delete_user_session(last_session)

        user_session_db = self.user_session_from_domain(user_session)

        self.db.add(user_session_db)
        self.db.commit()
        self.db.refresh(user_session_db)

        return self.user_session_to_domain(user_session_db)

    def get_user_session_by_id(self, user_id: int) -> UserSession | None:
        user_session_db = self.db.query(UserSessionDB).get(user_id)
        if user_session_db is None:
            return None
        return self.user_session_to_domain(user_session_db)

    def get_user_session_by_token(self, jwt_token: str) -> UserSession | None:
        user_session_db = (
            self.db.query(UserSessionDB)
            .filter(UserSessionDB.jwt_token == jwt_token)
            .first()
        )

        if user_session_db is not None:
            return self.user_session_to_domain(user_session_db)

        return None
