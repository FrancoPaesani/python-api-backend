from domain.user import User
from persistence.repositories.user_repository import UserRepository
from domain.user_patient import UserPatient
from schemas.patient_schema import UserPatientRequest
from domain.patient import Patient
from persistence.repositories.user_patient_repository import UserPatientsRepository


class UserPatientsService:
    def __init__(
        self,
        userpatients_repository: UserPatientsRepository,
        user_repository: UserRepository,
    ):
        self.userpatients_repository = userpatients_repository
        self.user_repository = user_repository

    def assign_patient_to_user(self, user_patient: UserPatientRequest) -> UserPatient:
        new_user_patient = UserPatient(
            user_id=user_patient.user_id, patient_id=user_patient.patient_id
        )

        patients_from_user: list[Patient] = (
            self.userpatients_repository.get_user_patients(user_id=user_patient.user_id)
        )
        patient_exists = (
            len(
                list(
                    filter(
                        lambda x: x.id == user_patient.patient_id, patients_from_user
                    )
                )
            )
            == 1
        )

        if patient_exists:
            raise ValueError(
                "El paciente ya se encuentra asignado al usuario ingresado"
            )

        return self.userpatients_repository.create_user_patient(new_user_patient)

    def retrieve_user_patients(self, user_id: int) -> User:
        patients = self.userpatients_repository.get_user_patients(user_id)
        user = self.user_repository.get_user_by_id(user_id)

        user.patients = patients

        return user
