import random
from faker import Faker

from domain.patient import PatientVitalSigns

fake = Faker()


def test_create_patient_vital_signs_successfully():
    systolic_pressure = random.random()
    vital_signs = PatientVitalSigns(
        patient_id=random.randint(1, 10),
        temperature=random.random(),
        systolic_pressure=systolic_pressure,
        diastolic_pressure=fake.random_int(min=80, max=120),
        pulse_rate=random.random(),
        respiration_rate=random.random(),
        height=random.random(),
        weight=random.random(),
    )

    assert vital_signs.systolic_pressure == systolic_pressure


def test_create_patient_vital_signs_then_increment_temperature_by_one():
    temperature = random.random()
    vital_signs = PatientVitalSigns(
        patient_id=random.randint(1, 10),
        temperature=temperature,
        systolic_pressure=fake.random_int(min=80, max=120),
        diastolic_pressure=fake.random_int(min=80, max=120),
        pulse_rate=random.random(),
        respiration_rate=random.random(),
        height=random.random(),
        weight=random.random(),
    )

    vital_signs.set_temperature(temperature + 1)

    assert vital_signs.temperature == temperature + 1


def test_create_patient_vital_signs_then_increment_pressure_by_one():
    systolic_pressure = fake.random_int(min=80, max=120)
    vital_signs = PatientVitalSigns(
        patient_id=random.randint(1, 10),
        temperature=random.random(),
        systolic_pressure=systolic_pressure,
        diastolic_pressure=fake.random_int(min=80, max=120),
        pulse_rate=random.random(),
        respiration_rate=random.random(),
        height=random.random(),
        weight=random.random(),
    )

    vital_signs.set_systolic_pressure(systolic_pressure + 1)

    assert vital_signs.systolic_pressure == systolic_pressure + 1


def test_fail_to_create_patient_invalid_pressure():
    systolic_pressure = 0

    try:
        PatientVitalSigns(
            patient_id=random.randint(1, 10),
            temperature=random.random(),
            systolic_pressure=systolic_pressure,
            diastolic_pressure=fake.random_int(min=80, max=120),
            pulse_rate=random.random(),
            respiration_rate=random.random(),
            height=random.random(),
            weight=random.random(),
        )
    except Exception as e:
        assert type(e) is ValueError
