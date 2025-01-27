from datetime import date
import pytest
from unittest.mock import Mock
from faker import Faker
from domain.patient import PatientVitalSigns, Patient
from schemas.patient_schema import PatientVitalSignsRequest
from services.vital_signs_service import VitalSignsService

fake = Faker()


@pytest.fixture
def mock_vital_signs_repository():
    return Mock()


@pytest.fixture
def mock_patient_repository():
    return Mock()


@pytest.fixture
def vital_signs_service(mock_vital_signs_repository, mock_patient_repository):
    return VitalSignsService(
        vital_signs_repository=mock_vital_signs_repository,
        patient_repository=mock_patient_repository,
    )


def test_register_vital_signs_success(
    vital_signs_service, mock_patient_repository, mock_vital_signs_repository
):
    patient_id = fake.random_int(min=1, max=1000)
    patient = Patient(
        id=patient_id,
        dni=fake.unique.random_int(min=1, max=50000000),
        name=fake.name(),
        birth_date=fake.date_of_birth(),
        sex_id=fake.random_int(min=1, max=2),
        weight=80,
        height=1.60,
    )
    vital_signs_request = PatientVitalSignsRequest(
        patient_id=patient.id,
        temperature=fake.pyfloat(min_value=35.0, max_value=42.0),
        systolic_pressure=fake.random_int(min=80, max=120),
        diastolic_pressure=fake.random_int(min=80, max=120),
        pulse_rate=fake.random_int(min=60, max=100),
        respiration_rate=fake.random_int(min=12, max=20),
    )

    mock_patient_repository.get_patient_by_id.return_value = patient
    mock_vital_signs_repository.register_vital_signs.return_value = PatientVitalSigns(
        **vital_signs_request.dict(),
        weight=patient.weight,
        height=patient.height,
    )

    registered_vital_signs = vital_signs_service.register_vital_signs(
        vital_signs_request
    )

    assert registered_vital_signs.patient_id == vital_signs_request.patient_id
    assert registered_vital_signs.temperature == vital_signs_request.temperature
    mock_patient_repository.get_patient_by_id.assert_called_once_with(
        vital_signs_request.patient_id
    )
    mock_vital_signs_repository.register_vital_signs.assert_called_once()


def test_get_vital_signs(
    vital_signs_service, mock_vital_signs_repository, mock_patient_repository
):
    patient_id = fake.random_int(min=1, max=1000)
    patient_birth_date = date.today()

    patient = Patient(
        id=patient_id,
        dni=11111111,
        sex_id=1,
        name=fake.name() + "AAAAA",
        birth_date=patient_birth_date,
        weight=fake.pyfloat(min_value=1, max_value=100),
        height=fake.pyfloat(min_value=1, max_value=2),
    )

    vital_signs = [
        PatientVitalSigns(
            patient_id=patient_id,
            temperature=fake.pyfloat(min_value=35.0, max_value=42.0),
            systolic_pressure=fake.random_int(min=80, max=120),
            diastolic_pressure=fake.random_int(min=80, max=120),
            pulse_rate=fake.random_int(min=60, max=100),
            respiration_rate=fake.random_int(min=12, max=20),
            weight=80,
            height=1.60,
        )
        for _ in range(3)
    ]

    mock_patient_repository.get_patient_by_id.return_value = patient

    mock_vital_signs_repository.get_vital_signs.return_value = vital_signs

    retrieved_vital_signs = vital_signs_service.get_vital_signs(patient_id)

    assert len(retrieved_vital_signs) == 3
    mock_vital_signs_repository.get_vital_signs.assert_called_once_with(patient_id)
