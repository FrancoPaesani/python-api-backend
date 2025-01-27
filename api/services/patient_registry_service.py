from schemas.patient_schema import PatientRegistryRequest
from domain.patient_registry import PatientRegistry
from persistence.repositories.patient_registry_repository import (
    PatientRegistryRepository,
)


class PatientRegistryService:
    def __init__(
        self,
        patient_registry_repository: PatientRegistryRepository,
    ):
        self.patient_registry_repository = patient_registry_repository

    def register_action(
        self, patient_registry: PatientRegistryRequest
    ) -> PatientRegistry:
        new_patient_registry = PatientRegistry(
            patient_id=patient_registry.patient_id,
            action_id=patient_registry.action_id,
            comment=patient_registry.comment,
        )
        patient_registry = self.patient_registry_repository.register_action(
            new_patient_registry
        )

        return patient_registry

    def get_patient_registry(self, patient_id: int) -> list[PatientRegistry]:
        return self.patient_registry_repository.get_patient_registry(patient_id)
