from persistence.repositories.patient_repository import PatientRepository
from domain.patient import Patient
from schemas.patient_schema import (
    PatientRequest,
    PatientUpdateRequest,
)


class PatientService:
    def __init__(
        self,
        patient_repository: PatientRepository,
    ):
        self.patient_repository = patient_repository

    def create_patient(self, patient: PatientRequest) -> Patient:
        new_patient = Patient(
            dni=patient.dni,
            name=patient.name,
            birth_date=patient.birth_date,
            sex_id=patient.sex_id,
            weight=patient.weight,
            height=patient.height,
        )

        if self.patient_repository.get_patient_by_dni(patient.dni) is not None:
            raise ValueError(
                "El DNI " + str(patient.dni) + " ya se encuentra registrado"
            )

        return self.patient_repository.create_patient(new_patient)

    def update_patient(self, patient: PatientUpdateRequest) -> Patient:
        patient_fields = patient.__dict__
        if patient.dni is not None:
            result: Patient | None = self.patient_repository.get_patient_by_dni(
                patient.dni
            )
            if result is not None and result.id != patient.id:
                raise ValueError(
                    "El DNI "
                    + str(patient.dni)
                    + " ya se encuentra registrado con otro paciente"
                )
        updated_patient = self.patient_repository.update_patient(patient_fields)

        return updated_patient
