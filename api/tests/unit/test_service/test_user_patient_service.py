import pytest
from unittest.mock import Mock
from faker import Faker
from domain.user_patient import UserPatient
from domain.patient import Patient
from schemas.patient_schema import UserPatientRequest
from services.user_patient_service import UserPatientsService

fake = Faker()


@pytest.fixture
def mock_userpatients_repository():
    return Mock()


@pytest.fixture
def mock_user_repository():
    return Mock()


def create_patient(patient_id) -> Patient:
    weight = fake.random_number(digits=2, fix_len=False)
    while weight < 0:
        weight = fake.random_number(digits=2, fix_len=False)
    height = height = fake.random_number(digits=3, fix_len=False) / 10
    while height < 0:
        height = height = fake.random_number(digits=3, fix_len=False) / 10
    return Patient(
        id=patient_id,
        dni=fake.unique.random_int(min=10000000, max=99999999),
        name=fake.name(),
        birth_date=fake.date_of_birth(),
        sex_id=fake.random_int(min=1, max=2),
        weight=weight,
        height=height,
    )


@pytest.fixture
def user_patients_service(mock_userpatients_repository, mock_user_repository):
    return UserPatientsService(
        userpatients_repository=mock_userpatients_repository,
        user_repository=mock_user_repository,
    )


def test_assign_patient_to_user_success(
    user_patients_service, mock_userpatients_repository
):
    user_patient_request = UserPatientRequest(
        user_id=fake.random_int(min=1, max=1000),
        patient_id=fake.random_int(min=1, max=1000),
    )
    patients_from_user = []

    mock_userpatients_repository.get_user_patients.return_value = patients_from_user
    mock_userpatients_repository.create_user_patient.return_value = UserPatient(
        user_id=user_patient_request.user_id,
        patient_id=user_patient_request.patient_id,
    )

    assigned_user_patient = user_patients_service.assign_patient_to_user(
        user_patient_request
    )

    assert assigned_user_patient.user_id == user_patient_request.user_id
    assert assigned_user_patient.patient_id == user_patient_request.patient_id
    mock_userpatients_repository.get_user_patients.assert_called_once_with(
        user_id=user_patient_request.user_id
    )
    mock_userpatients_repository.create_user_patient.assert_called_once()


def test_assign_patient_to_user_duplicate(
    user_patients_service, mock_userpatients_repository
):
    user_patient_request = UserPatientRequest(
        user_id=fake.random_int(min=1, max=1000),
        patient_id=fake.random_int(min=1, max=1000),
    )
    patients_from_user = [create_patient(user_patient_request.patient_id)]

    mock_userpatients_repository.get_user_patients.return_value = patients_from_user

    with pytest.raises(
        ValueError, match="El paciente ya se encuentra asignado al usuario ingresado"
    ):
        user_patients_service.assign_patient_to_user(user_patient_request)

    mock_userpatients_repository.get_user_patients.assert_called_once_with(
        user_id=user_patient_request.user_id
    )
    mock_userpatients_repository.create_user_patient.assert_not_called()


def test_retrieve_user_patients(
    user_patients_service, mock_userpatients_repository, mock_user_repository
):
    user_id = fake.random_int(min=1, max=1000)
    patients = [create_patient(fake.random_int(min=1, max=1000)) for _ in range(3)]
    user = Mock()
    user.patients = patients

    mock_userpatients_repository.get_user_patients.return_value = patients
    mock_user_repository.get_user_by_id.return_value = user

    user = user_patients_service.retrieve_user_patients(user_id)

    assert len(user.patients) == 3
    assert user.patients == patients
    mock_userpatients_repository.get_user_patients.assert_called_once_with(user_id)
    mock_user_repository.get_user_by_id.assert_called_once_with(user_id)
