from datetime import date
from decimal import Decimal
from typing import Union

from domain.vital_signs_info import (
    PressureInfo,
    PulseRateInfo,
    RespirationRateInfo,
    TemperatureInfo,
)


class Patient:
    def __init__(
        self,
        dni: int,
        name: str,
        birth_date: date,
        sex_id: int,
        id: int | None = None,
        weight: Decimal | None = None,
        height: Decimal | None = None,
    ):
        self.set_dni(dni)
        self.set_name(name)
        self.set_birth_date(birth_date)
        self.sex_id = sex_id
        self.id = id
        self.set_weight(weight)
        self.set_height(height)

    @classmethod
    def from_dict(cls, fields: dict):
        patient = object.__new__(Patient)
        for x in fields:
            setattr(patient, x[0], x[1])
        return patient

    def set_dni(self, dni: int):
        if dni <= 0:
            raise ValueError("Ingrese un documento válido.")
        self.dni = dni

    def set_name(self, name: str):
        if len(name) <= 2:
            raise ValueError("El nombre debe tener al menos 3 caracteres.")
        self.name = name

    def set_birth_date(self, birth_date: date):
        if birth_date > date.today():
            raise ValueError("La fecha de nacimiento debe ser igual o anterior a hoy.")
        self.birth_date = birth_date

    def set_weight(self, weight: Decimal | None):
        if weight is not None and weight <= 0:
            raise ValueError("El peso del paciente debe ser mayor a cero.")
        self.weight = weight

    def set_height(self, height: Decimal | None):
        if height is not None and height <= 0:
            raise ValueError("La altura del paciente debe ser mayor a cero.")
        self.height = height


class PatientVitalSigns:
    info: (
        list[
            Union[
                PressureInfo, PulseRateInfo, RespirationRateInfo, TemperatureInfo, dict
            ]
        ]
        | None
    ) = None

    def __init__(
        self,
        patient_id: int,
        temperature: Decimal,
        systolic_pressure: Decimal,
        diastolic_pressure: Decimal,
        pulse_rate: Decimal,
        respiration_rate: Decimal,
        weight: Decimal | None,
        height: Decimal | None,
        vitalsign_id: int | None = None,
    ):
        self.vitalsign_id = vitalsign_id
        self.patient_id = patient_id
        self.set_temperature(temperature)
        self.set_systolic_pressure(systolic_pressure)
        self.set_diastolic_pressure(diastolic_pressure)
        self.set_pulse_rate(pulse_rate)
        self.set_respiration_rate(respiration_rate)
        self.set_weight(weight)
        self.set_height(height)

    def set_temperature(self, temperature: Decimal):
        if temperature <= 0:
            raise ValueError("La temperatura debe ser mayor a cero.")
        self.temperature = temperature

    def set_systolic_pressure(self, systolic_pressure: Decimal):
        if systolic_pressure <= 0:
            raise ValueError("La presión debe ser mayor a cero.")
        self.systolic_pressure = systolic_pressure

    def set_diastolic_pressure(self, diastolic_pressure: Decimal):
        if diastolic_pressure <= 0:
            raise ValueError("La presión debe ser mayor a cero.")
        self.diastolic_pressure = diastolic_pressure

    def set_pulse_rate(self, pulse_rate: Decimal):
        if pulse_rate <= 0:
            raise ValueError("El pulso debe ser mayor a cero.")
        self.pulse_rate = pulse_rate

    def set_respiration_rate(self, respiration_rate: Decimal):
        if respiration_rate <= 0:
            raise ValueError("El ritmo respiratorio debe ser mayor a cero.")
        self.respiration_rate = respiration_rate

    def set_weight(self, weight: Decimal | None):
        if weight is not None and weight <= 0:
            raise ValueError("El peso debe ser mayor a cero.")
        self.weight = weight

    def set_height(self, height: Decimal | None):
        if height is not None and height <= 0:
            raise ValueError("La altura debe ser mayor a cero.")
        self.height = height
