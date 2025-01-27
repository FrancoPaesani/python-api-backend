import pytest
from unittest.mock import Mock
from faker import Faker
from domain.patient import Patient
from schemas.patient_schema import PatientRequest, PatientUpdateRequest
from services.patient_service import PatientService

fake = Faker()


@pytest.fixture
def mock_patient_repository():
    return Mock()


@pytest.fixture
def patient_service(mock_patient_repository):
    return PatientService(patient_repository=mock_patient_repository)


def create_patient() -> PatientRequest:
    name = fake.name().upper()
    while len(name) < 10:
        name = fake.name().upper()
    weight = fake.random_number(digits=2, fix_len=False)
    while weight <= 0:
        weight = fake.random_number(digits=2, fix_len=False)
    height = height = fake.random_number(digits=3, fix_len=False) / 10
    while height <= 0:
        height = height = fake.random_number(digits=3, fix_len=False) / 10

    return PatientRequest(
        dni=fake.random_int(min=10000000, max=99999999),
        name=name,
        birth_date=fake.date_of_birth(minimum_age=1, maximum_age=90).isoformat(),
        sex_id=fake.random_int(min=1, max=2),
        weight=weight,
        height=height,
    )


def create_patient_update() -> PatientUpdateRequest:
    name = fake.name().upper()
    while len(name) < 10:
        name = fake.name().upper()
    weight = fake.random_number(digits=2, fix_len=False)
    while weight <= 0:
        weight = fake.random_number(digits=2, fix_len=False)
    height = height = fake.random_number(digits=3, fix_len=False) / 10
    while height <= 0:
        height = height = fake.random_number(digits=3, fix_len=False) / 10

    return PatientUpdateRequest(
        id=fake.random_int(min=1, max=1000),
        dni=fake.random_int(min=10000000, max=99999999),
        name=name,
        birth_date=fake.date_of_birth(minimum_age=1, maximum_age=90).isoformat(),
        sex_id=fake.random_int(min=1, max=2),
        weight=weight,
        height=weight,
    )


def test_create_patient_successfully(patient_service, mock_patient_repository):
    patient_request = create_patient()

    mock_patient_repository.get_patient_by_dni.return_value = None
    mock_patient_repository.create_patient.return_value = Patient(
        id=fake.random_int(min=1, max=1000),
        dni=patient_request.dni,
        name=patient_request.name,
        birth_date=patient_request.birth_date,
        sex_id=patient_request.sex_id,
        weight=patient_request.weight,
        height=patient_request.height,
    )

    created_patient = patient_service.create_patient(patient_request)

    assert created_patient.dni == patient_request.dni
    assert created_patient.name == patient_request.name
    mock_patient_repository.get_patient_by_dni.assert_called_once_with(
        patient_request.dni
    )
    mock_patient_repository.create_patient.assert_called_once()


def test_fail_to_create_patient_duplicate_dni(patient_service, mock_patient_repository):
    patient_request = create_patient()

    mock_patient_repository.get_patient_by_dni.return_value = Patient(
        id=fake.random_int(min=1, max=1000),
        dni=patient_request.dni,
        name=fake.name(),
        birth_date=fake.date_of_birth(minimum_age=1, maximum_age=99),
        sex_id=fake.random_int(min=1, max=2),
        weight=fake.random_number(digits=2),
        height=fake.random_number(digits=3),
    )

    with pytest.raises(
        ValueError, match=f"El DNI {patient_request.dni} ya se encuentra registrado"
    ):
        patient_service.create_patient(patient_request)

    mock_patient_repository.get_patient_by_dni.assert_called_once_with(
        patient_request.dni
    )
    mock_patient_repository.create_patient.assert_not_called()


def test_update_patient_successfully(patient_service, mock_patient_repository):
    patient_update_request = create_patient_update()

    mock_patient_repository.get_patient_by_dni.return_value = None
    mock_patient_repository.update_patient.return_value = Patient(
        id=patient_update_request.id,
        dni=patient_update_request.dni,
        name=patient_update_request.name,
        birth_date=patient_update_request.birth_date,
        sex_id=patient_update_request.sex_id,
        weight=patient_update_request.weight,
        height=patient_update_request.height,
    )

    updated_patient = patient_service.update_patient(patient_update_request)

    assert updated_patient.id == patient_update_request.id
    assert updated_patient.dni == patient_update_request.dni
    mock_patient_repository.get_patient_by_dni.assert_called_once_with(
        patient_update_request.dni
    )
    mock_patient_repository.update_patient.assert_called_once_with(
        patient_update_request.__dict__
    )


def test_fail_to_update_patient_duplicate_dni(patient_service, mock_patient_repository):
    existing_patient_id = fake.random_int(min=1, max=1000)
    patient_update_request = create_patient_update()

    mock_patient_repository.get_patient_by_dni.return_value = Patient(
        id=existing_patient_id,
        dni=patient_update_request.dni,
        name=fake.name(),
        birth_date=fake.date_of_birth(minimum_age=1, maximum_age=99),
        sex_id=fake.random_int(min=1, max=2),
        weight=fake.random_number(digits=2),
        height=fake.random_number(digits=3),
    )

    with pytest.raises(
        ValueError,
        match=f"El DNI {patient_update_request.dni} ya se encuentra registrado con otro paciente",
    ):
        patient_service.update_patient(patient_update_request)

    mock_patient_repository.get_patient_by_dni.assert_called_once_with(
        patient_update_request.dni
    )
    mock_patient_repository.update_patient.assert_not_called()
