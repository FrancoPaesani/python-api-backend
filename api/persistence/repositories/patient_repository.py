from sqlalchemy.orm import Session

from persistence.models.patients_models import (
    PatientDB,
    UserPatientsDB,
)
from domain.patient import Patient


class PatientRepository:
    def __init__(self, db: Session):
        self.db = db

    @classmethod
    def from_domain(cls, patient: Patient) -> PatientDB:
        return PatientDB(
            id=patient.id,
            dni=patient.dni,
            name=patient.name,
            birth_date=patient.birth_date,
            sex_id=patient.sex_id,
            weight=patient.weight,
            height=patient.height,
        )

    @classmethod
    def to_domain(cls, patient: UserPatientsDB) -> Patient:
        return Patient(
            id=patient.id,
            dni=patient.dni,
            name=patient.name,
            birth_date=patient.birth_date,
            sex_id=patient.sex_id,
            weight=patient.weight,
            height=patient.height,
        )

    def create_patient(self, patient: Patient) -> Patient:
        patient_db = PatientRepository.from_domain(patient)

        self.db.add(patient_db)
        self.db.commit()
        self.db.refresh(patient_db)

        patient.id = patient_db.id
        return patient

    def update_patient(self, patient_fields: dict) -> Patient:
        patient_db: PatientDB = self.db.query(PatientDB).get(patient_fields["id"])

        for x in patient_fields.items():
            if x[1] is not None:
                setattr(patient_db, x[0], x[1])

        self.db.commit()
        self.db.refresh(patient_db)

        return PatientRepository.to_domain(patient_db)

    def get_patient_by_dni(self, patient_dni: int) -> Patient | None:
        patient_db = (
            self.db.query(PatientDB).filter(PatientDB.dni == patient_dni).first()
        )
        if patient_db is not None:
            return PatientRepository.to_domain(patient_db)
        return None

    def get_patient_by_id(self, patient_id: int) -> Patient | None:
        patient_db = self.db.query(PatientDB).get(patient_id)
        if patient_db is not None:
            return PatientRepository.to_domain(patient_db)
        return None
