from pydantic import BaseModel, field_validator

from schemas.patient_schema import PatientResponse


class UserBase(BaseModel):
    code: str
    name: str
    email: str

    @field_validator("name", mode="before")
    @classmethod
    def to_uppercase(cls, value: str) -> str:
        if value is not None:
            return value.upper()
        return value

    @field_validator("email", mode="before")
    @classmethod
    def to_lowercase(cls, value: str) -> str:
        if value is not None:
            return value.lower()
        return value


class UserRequest(UserBase):
    hashed_password: str


class UserResponse(UserBase):
    id: int
    active: bool
    patients: list[PatientResponse] | None = None


class PermissionBase(BaseModel):
    code: str
    name: str

    @field_validator("code", "name", mode="before")
    @classmethod
    def to_uppercase(cls, value: str) -> str:
        if value is not None:
            return value.upper()
        return value


class PermissionRequest(PermissionBase):
    pass


class PermissionResponse(PermissionBase):
    id: int


class LoginUserRequest(BaseModel):
    code: str
    hashed_password: str


class LoginUserResponse(UserBase):
    id: int
    permissions: list[PermissionResponse]
