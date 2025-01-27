from persistence.repositories.patient_repository import PatientRepository
from domain.patient import Patient
from domain.user_patient import UserPatient
from persistence.models.patients_models import PatientDB, UserPatientsDB
from sqlalchemy.orm import Session


class UserPatientsRepository:
    def __init__(self, db: Session):
        self.db = db

    @classmethod
    def from_domain(cls, user_patient: UserPatient) -> UserPatientsDB:
        return UserPatientsDB(
            user_id=user_patient.user_id, patient_id=user_patient.patient_id
        )

    @classmethod
    def to_domain(cls, user_patient: UserPatientsDB) -> UserPatient:
        return UserPatient(
            user_id=user_patient.user_id, patient_id=user_patient.patient_id
        )

    def get_user_patients(self, user_id: int) -> list[Patient]:
        patients_db = (
            self.db.query(PatientDB)
            .join(UserPatientsDB)
            .filter(UserPatientsDB.user_id == user_id)
            .all()
        )
        patients = list(map(lambda x: PatientRepository.to_domain(x), patients_db))
        return patients

    def create_user_patient(self, user_patient: UserPatient) -> UserPatient:
        user_patient_db = UserPatientsRepository.from_domain(user_patient)

        self.db.add(user_patient_db)
        self.db.commit()
        self.db.refresh(user_patient_db)

        return user_patient
