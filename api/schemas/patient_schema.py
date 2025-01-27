from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, field_validator


class PatientBase(BaseModel):
    dni: int
    name: str
    birth_date: date
    sex_id: int
    weight: Decimal
    height: Decimal

    @field_validator("name", mode="before")
    @classmethod
    def to_uppercase(cls, value: str) -> str:
        if value is not None:
            return value.upper()
        return value


class PatientRequest(PatientBase):
    pass


class PatientResponse(PatientBase):
    id: int


class PatientUpdateRequest(PatientBase):
    id: int
    dni: int = None
    name: str = None
    birth_date: date = None
    sex_id: int = None
    weight: Decimal = None
    height: Decimal = None

    @field_validator("name", mode="before")
    @classmethod
    def to_uppercase(cls, value: str) -> str:
        if value is not None:
            return value.upper()
        return value


class UserPatientRequest(BaseModel):
    user_id: int
    patient_id: int


class UserPatientResponse(UserPatientRequest):
    pass


class PatientVitalSignsBase(BaseModel):
    patient_id: int
    temperature: Decimal
    systolic_pressure: Decimal
    diastolic_pressure: Decimal
    pulse_rate: Decimal
    respiration_rate: Decimal


class PatientVitalSignsRequest(PatientVitalSignsBase):
    pass


class PatientVitalSignsResponse(PatientVitalSignsBase):
    vitalsign_id: int
    weight: Decimal
    height: Decimal
    info: list[dict]


class PatientRegistryBase(BaseModel):
    patient_id: int
    action_id: int
    comment: str


class PatientRegistryRequest(PatientRegistryBase):
    pass


class PatientRegistryResponse(PatientRegistryBase):
    id: int
    timestamp: datetime
    user_id: int | None
