from datetime import datetime
import random
from faker import Faker

from domain.patient_registry import PatientRegistry

fake = Faker()


def test_create_patient_registry():
    comment = fake.text()
    patient_registry = PatientRegistry(
        patient_id=random.randint(1, 2),
        action_id=random.randint(1, 2),
        comment=comment,
    )

    assert patient_registry.comment == comment


def test_create_patient_registry_with_timestamp():
    comment = fake.text()
    patient_registry = PatientRegistry(
        patient_id=random.randint(1, 2),
        action_id=random.randint(1, 2),
        comment=comment,
        timestamp=datetime.now(),
    )

    assert patient_registry.comment == comment
