from datetime import datetime
from utils.date_utils import (
    diff_in_months_date,
    diff_in_years_date,
)
from domain.vital_signs_info import (
    TemperatureInfo,
    PressureInfo,
    PulseRateInfo,
    RespirationRateInfo,
)
from persistence.repositories.patient_repository import PatientRepository
from domain.patient import Patient, PatientVitalSigns
from persistence.repositories.vital_signs_repository import VitalSignsRepository
from schemas.patient_schema import PatientVitalSignsRequest


class VitalSignsService:
    def __init__(
        self,
        vital_signs_repository: VitalSignsRepository,
        patient_repository: PatientRepository,
    ):
        self.vital_signs_repository = vital_signs_repository
        self.patient_repository = patient_repository

    def parse_vital_signs_info(
        self, patient: Patient, vital_signs: PatientVitalSigns
    ) -> PatientVitalSigns:
        print(patient.birth_date)
        age_in_months = diff_in_months_date(patient.birth_date, datetime.now())
        age_in_years = diff_in_years_date(patient.birth_date, datetime.now())

        temperature_info = TemperatureInfo(temperature=vital_signs.temperature)
        pressure_info = PressureInfo(
            systolic=vital_signs.systolic_pressure,
            diastolic=vital_signs.diastolic_pressure,
        )
        pulse_rate_info = PulseRateInfo(
            pulse_rate=vital_signs.pulse_rate, age_in_months=age_in_months
        )
        respiration_rate_info = RespirationRateInfo(
            respiration_rate=vital_signs.respiration_rate, age_in_years=age_in_years
        )

        vital_signs.info = [
            temperature_info,
            pressure_info,
            pulse_rate_info,
            respiration_rate_info,
        ]

        return vital_signs

    def register_vital_signs(
        self, vital_signs: PatientVitalSignsRequest
    ) -> PatientVitalSigns:
        patient = self.patient_repository.get_patient_by_id(vital_signs.patient_id)

        if patient is None:
            raise ValueError("El paciente no existe.")

        new_vital_signs = PatientVitalSigns(
            patient_id=vital_signs.patient_id,
            temperature=vital_signs.temperature,
            systolic_pressure=vital_signs.systolic_pressure,
            diastolic_pressure=vital_signs.diastolic_pressure,
            pulse_rate=vital_signs.pulse_rate,
            respiration_rate=vital_signs.respiration_rate,
            weight=patient.weight,
            height=patient.height,
        )

        registered_vital_signs = self.vital_signs_repository.register_vital_signs(
            new_vital_signs
        )

        parsed_vital_signs: PatientVitalSigns = self.parse_vital_signs_info(
            patient, registered_vital_signs
        )

        return parsed_vital_signs

    def get_vital_signs(self, patient_id: int) -> list[PatientVitalSigns]:
        patient = self.patient_repository.get_patient_by_id(patient_id)

        if patient is None:
            raise ValueError("El paciente no existe.")

        vital_signs: list[PatientVitalSigns] = (
            self.vital_signs_repository.get_vital_signs(patient_id)
        )

        vital_signs = list(
            map(lambda x: self.parse_vital_signs_info(patient, x), vital_signs)
        )
        # for x in vital_signs:
        #     x: PatientVitalSigns = self.parse_vital_signs_info(patient, x)

        return vital_signs
