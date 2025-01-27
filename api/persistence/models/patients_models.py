from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Identity,
    Integer,
    Numeric,
    String,
)

from ..database import Base


class PatientDB(Base):
    __tablename__ = "patients"
    id = Column(Integer, Identity(always=True), primary_key=True, index=True)
    dni = Column(BigInteger, unique=True)
    name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    sex_id = Column(ForeignKey("sex.id"))
    weight = Column(Numeric)
    height = Column(Numeric)
    date_created = Column(DateTime, nullable=False, default=datetime.now)


class SexDB(Base):
    __tablename__ = "sex"
    id = Column(Integer, Identity(always=True), primary_key=True, index=True)
    description = Column(String, nullable=False)


class PatientVitalSignsDB(Base):
    __tablename__ = "patient_vital_signs"
    vitalsign_id = Column(Integer, Identity(always=True), primary_key=True, index=True)
    patient_id = Column(ForeignKey("patients.id"))
    temperature = Column(Numeric)
    systolic_pressure = Column(Numeric)
    diastolic_pressure = Column(Numeric)
    pulse_rate = Column(Numeric)
    respiration_rate = Column(Numeric)
    weight = Column(Numeric)
    height = Column(Numeric)
    date_created = Column(DateTime, nullable=False, default=datetime.now)


class UserPatientsDB(Base):
    __tablename__ = "user_patients"
    user_id = Column(ForeignKey("users.id"), primary_key=True)
    patient_id = Column(ForeignKey("patients.id"), primary_key=True)
    date_created = Column(DateTime, nullable=False, default=datetime.now)


class PatientRegistryDB(Base):
    __tablename__ = "patient_registry"
    id = Column(Integer, Identity(always=True), primary_key=True, index=True)
    patient_id = Column(ForeignKey("patients.id"))
    action_id = Column(ForeignKey("actions.id"))
    comment = Column(String)
    timestamp = Column(DateTime, nullable=False, default=datetime.now)
    user_id = Column(ForeignKey("users.id"))


class ActionsDB(Base):
    __tablename__ = "actions"
    id = Column(Integer, Identity(always=True), primary_key=True, index=True)
    description = Column(String)
    date_created = Column(DateTime, nullable=False, default=datetime.now)
