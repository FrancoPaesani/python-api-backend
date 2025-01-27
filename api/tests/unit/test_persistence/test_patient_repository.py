import random
from faker import Faker

from persistence.models.patients_models import PatientDB
from persistence.repositories.patient_repository import PatientRepository

fake = Faker()


def test_create_patient(db_session):
    patient_repo = PatientRepository(db_session)

    dni, name, birth_date, sex_id, weight, height = (
        random.randint(1, 50000000),
        fake.name(),
        fake.date_of_birth(),
        random.randint(1, 2),
        random.random(),
        random.random(),
    )

    new_patient = PatientDB(
        dni=dni,
        name=name,
        birth_date=birth_date,
        sex_id=sex_id,
        weight=weight,
        height=height,
    )
    new_patient = patient_repo.create_patient(patient_repo.to_domain(new_patient))
    new_patient = patient_repo.get_patient_by_id(new_patient.id)

    assert new_patient is not None
    assert new_patient.name == name


def test_create_patient_then_update(db_session):
    patient_repo = PatientRepository(db_session)

    dni, name, birth_date, sex_id, weight, height = (
        random.randint(1, 50000000),
        fake.name(),
        fake.date_of_birth(),
        random.randint(1, 2),
        random.random(),
        random.random(),
    )

    new_patient = PatientDB(
        dni=dni,
        name=name,
        birth_date=birth_date,
        sex_id=sex_id,
        weight=weight,
        height=height,
    )
    new_patient = patient_repo.create_patient(patient_repo.to_domain(new_patient))

    updated_patient = patient_repo.update_patient(
        {"id": new_patient.id, "name": fake.name()}
    )
    updated_patient = patient_repo.get_patient_by_dni(updated_patient.dni)

    assert new_patient.id == updated_patient.id
    assert new_patient.name != updated_patient.name
