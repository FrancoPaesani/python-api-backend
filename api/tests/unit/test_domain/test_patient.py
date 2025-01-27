import random
from faker import Faker

from domain.patient import Patient

fake = Faker()


def test_create_patient_successfull_without_height_nor_weight():
    name = fake.name()
    while len(name) < 3:
        name = fake.name()
    patient = Patient(
        dni=random.randint(1, 50000000),
        name=name,
        birth_date=fake.date_of_birth(),
        sex_id=random.randint(1, 2),
    )

    assert patient.name == name


def test_create_patient_successfull_with_height_and_weight():
    name = fake.name()
    while len(name) < 3:
        name = fake.name()
    patient = Patient(
        dni=random.randint(1, 50000000),
        name=name,
        birth_date=fake.date_of_birth(),
        sex_id=random.randint(1, 2),
        height=random.random(),
        weight=random.random(),
    )

    assert patient.name == name


def test_failt_to_create_patient_invalid_dni():
    name = fake.name()
    while len(name) < 3:
        name = fake.name()

    try:
        Patient(
            dni=random.randint(-50000000, 0),
            name=name,
            birth_date=fake.date_of_birth(),
            sex_id=random.randint(1, 2),
            height=random.random(),
            weight=random.random(),
        )
    except Exception as e:
        assert type(e) is ValueError
