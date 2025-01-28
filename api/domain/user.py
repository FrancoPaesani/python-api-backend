from datetime import datetime

from email_validator import validate_email

from domain.patient import Patient
from domain.permission import Permission


class User:
    patients: list[Patient] | None = None

    def __init__(
        self,
        code: str,
        name: str,
        email: str,
        hashed_password: str,
        id: int | None = None,
        active: bool | None = None,
    ):
        self.id = id
        self.set_code(code)
        self.set_name(name)
        self.set_email(email)
        self.set_hashed_password(hashed_password)
        self.active = active

    def set_code(self, code: str):
        if len(code) <= 2:
            raise ValueError("El código del usuario de tener más de dos caracteres.")
        if " " in code:
            raise ValueError("El código no debe contener espacios.")
        self.code = code

    def set_name(self, name: str):
        if len(name) <= 5:
            raise ValueError("El nombre debe contener al menos 6 caracteres.")
        self.name = name

    def set_email(self, email: str):
        try:
            emailinfo = validate_email(email, check_deliverability=False)
            self.email = emailinfo.email
        except Exception:
            raise ValueError("El email no es válido.")

    def set_hashed_password(self, hashed_password: str):
        self.hashed_password = hashed_password


class UserPermission:
    def __init__(
        self,
        user_id: int,
        permission_id: int,
        date_created: datetime,
        user_created: int,
    ):
        self.user_id = user_id
        self.permission_id = permission_id
        self.date_created = date_created
        self.user_created = user_created


class UserSession:
    def __init__(
        self,
        user_id: int,
        jwt_token: str,
        expiry_date: datetime,
        created: datetime | None = None,
    ):
        self.user_id = user_id
        self.jwt_token = jwt_token
        self.set_expiry_date(expiry_date)
        self.created = created

    def set_expiry_date(self, expiry_date: datetime):
        if datetime.now() >= expiry_date:
            raise ValueError(
                "La fecha de vencimiento de la sesión debe ser posterior a este instante."
            )
        self.expiry_date = expiry_date


class UserWithPermissions(User):
    permissions: list[Permission] | None
    jwt_token: str

    def __init__(
        self,
        code,
        name,
        email,
        hashed_password=None,
        permissions: list[Permission] | None = None,
        id=None,
        active=None,
    ):
        super().__init__(code, name, email, hashed_password, id, active)
        self.permissions = permissions
