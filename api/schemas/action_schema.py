from pydantic import BaseModel, field_validator


class ActionBase(BaseModel):
    description: str

    @field_validator("description", mode="before")
    @classmethod
    def to_uppercase(cls, value: str) -> str:
        if value is not None:
            return value.upper()
        return value


class ActionRequest(ActionBase):
    pass


class ActionResponse(ActionBase):
    id: int
