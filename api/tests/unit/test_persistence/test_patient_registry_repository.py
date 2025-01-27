import random
from faker import Faker

from persistence.models.patients_models import PatientDB, PatientRegistryDB
from persistence.repositories.patient_repository import PatientRepository
from persistence.repositories.patient_registry_repository import (
    PatientRegistryRepository,
)

fake = Faker()


def test_create_patient_and_register_action(db_session):
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

    patient_registry_repository = PatientRegistryRepository(db_session)

    new_patient_registry = PatientRegistryDB(
        patient_id=new_patient.id,
        action_id=random.randint(1, 4),
        comment=fake.text(max_nb_chars=20),
    )

    new_patient_registry = patient_registry_repository.register_action(
        patient_registry_repository.to_domain(new_patient_registry)
    )

    patient_registry_db = patient_registry_repository.get_patient_registry(
        new_patient.id
    )

    assert len(patient_registry_db) == 1
