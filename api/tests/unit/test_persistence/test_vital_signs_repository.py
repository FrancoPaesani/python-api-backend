import random
from faker import Faker

from persistence.models.patients_models import PatientDB, PatientVitalSignsDB
from persistence.repositories.patient_repository import PatientRepository
from persistence.repositories.vital_signs_repository import VitalSignsRepository

fake = Faker()


def test_create_patient_and_register_vital_signs(db_session):
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

    vital_signs_repository = VitalSignsRepository(db_session)

    new_vital_signs = PatientVitalSignsDB(
        patient_id=new_patient.id,
        temperature=random.random(),
        systolic_pressure=fake.random_int(min=80, max=120),
        diastolic_pressure=fake.random_int(min=80, max=120),
        pulse_rate=random.random(),
        respiration_rate=random.random(),
        weight=random.random(),
        height=random.random(),
    )

    new_vital_signs = vital_signs_repository.register_vital_signs(
        vital_signs_repository.from_domain(new_vital_signs)
    )

    vital_signs_db = vital_signs_repository.get_vital_signs(new_patient.id)

    assert len(vital_signs_db) == 1
