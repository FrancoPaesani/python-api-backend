import random
from faker import Faker

from persistence.models.user_models import UserDB
from persistence.models.patients_models import PatientDB, UserPatientsDB
from persistence.repositories.patient_repository import PatientRepository
from persistence.repositories.user_repository import UserRepository
from persistence.repositories.user_patient_repository import UserPatientsRepository

fake = Faker()


def test_create_user_then_create_patient_and_assign_to_user(db_session):
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

    user_repo = UserRepository(db_session)

    code, name, email, hashed_password = (
        fake.name().upper()[0:3],
        fake.name(),
        fake.email(),
        fake.password(),
    )

    new_user = UserDB(
        code=code, name=name, email=email, hashed_password=hashed_password
    )
    user_repo.create_user(user_repo.user_to_domain(new_user))

    user_in_db = db_session.query(UserDB).filter_by(code=code).first()
    assert user_in_db is not None
    assert user_in_db.name == name

    user_patient_repository = UserPatientsRepository(db_session)

    user_patient = UserPatientsDB(user_id=user_in_db.id, patient_id=new_patient.id)

    user_patient = user_patient_repository.create_user_patient(
        user_patient_repository.from_domain(user_patient)
    )

    user_patients = user_patient_repository.get_user_patients(user_in_db.id)

    assert len(user_patients) == 1
