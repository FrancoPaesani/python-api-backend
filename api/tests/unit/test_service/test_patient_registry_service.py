from datetime import datetime
import pytest
from unittest.mock import Mock
from faker import Faker
from domain.patient_registry import PatientRegistry
from schemas.patient_schema import PatientRegistryRequest
from services.patient_registry_service import PatientRegistryService

fake = Faker()


@pytest.fixture
def mock_patient_registry_repository():
    return Mock()


@pytest.fixture
def patient_registry_service(mock_patient_registry_repository):
    return PatientRegistryService(
        patient_registry_repository=mock_patient_registry_repository
    )


def test_register_action_success(
    patient_registry_service, mock_patient_registry_repository
):
    patient_registry_request = PatientRegistryRequest(
        patient_id=fake.random_int(min=1, max=1000),
        action_id=fake.random_int(min=1, max=10),
        comment=fake.text(max_nb_chars=100),
    )
    patient_registry = PatientRegistry(
        patient_id=patient_registry_request.patient_id,
        action_id=patient_registry_request.action_id,
        comment=patient_registry_request.comment,
        id=fake.uuid4(),
        timestamp=datetime.now(),
    )

    mock_patient_registry_repository.register_action.return_value = patient_registry

    registered_action = patient_registry_service.register_action(
        patient_registry_request
    )

    assert registered_action.patient_id == patient_registry_request.patient_id
    assert registered_action.action_id == patient_registry_request.action_id
    assert registered_action.comment == patient_registry_request.comment
    mock_patient_registry_repository.register_action.assert_called_once()


def test_get_patient_registry_success(
    patient_registry_service, mock_patient_registry_repository
):
    patient_id = fake.random_int(min=1, max=1000)
    patient_registries = [
        PatientRegistry(
            patient_id=patient_id,
            action_id=fake.random_int(min=1, max=10),
            comment=fake.text(max_nb_chars=100),
        )
        for _ in range(3)
    ]

    mock_patient_registry_repository.get_patient_registry.return_value = (
        patient_registries
    )

    retrieved_registries = patient_registry_service.get_patient_registry(patient_id)

    assert len(retrieved_registries) == 3
    mock_patient_registry_repository.get_patient_registry.assert_called_once_with(
        patient_id
    )
