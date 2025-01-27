from sqlalchemy.orm import Session

from persistence.models.patients_models import PatientRegistryDB
from domain.patient_registry import PatientRegistry


class PatientRegistryRepository:
    def __init__(self, db: Session):
        self.db = db

    @classmethod
    def from_domain(cls, patient_registry: PatientRegistry) -> PatientRegistryDB:
        return PatientRegistryDB(
            id=patient_registry.id,
            patient_id=patient_registry.patient_id,
            action_id=patient_registry.action_id,
            comment=patient_registry.comment,
            timestamp=patient_registry.timestamp,
            user_id=patient_registry.user_id,
        )

    @classmethod
    def to_domain(cls, patient_registry: PatientRegistryDB) -> PatientRegistry:
        return PatientRegistry(
            id=patient_registry.id,
            patient_id=patient_registry.patient_id,
            action_id=patient_registry.action_id,
            comment=patient_registry.comment,
            timestamp=patient_registry.timestamp,
            user_id=patient_registry.user_id,
        )

    def register_action(self, patient_registry: PatientRegistry) -> PatientRegistry:
        patient_registry_db = PatientRegistryRepository.from_domain(patient_registry)

        self.db.add(patient_registry_db)
        self.db.commit()
        self.db.refresh(patient_registry_db)

        return PatientRegistryRepository.to_domain(patient_registry_db)

    def get_patient_registry(self, patient_id: int) -> list[PatientRegistry]:
        patient_registry_db: list[PatientRegistryDB] = (
            self.db.query(PatientRegistryDB)
            .filter(PatientRegistryDB.patient_id == patient_id)
            .all()
        )

        patient_registry = list(
            map(lambda x: PatientRegistryRepository.to_domain(x), patient_registry_db)
        )

        return patient_registry
