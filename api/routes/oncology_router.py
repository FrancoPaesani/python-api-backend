from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from decorators.auth_decorators import validate_login, validate_route_permission
from schemas.management_schema import UserResponse
from persistence.repositories.user_repository import UserRepository
from persistence.repositories.action_repository import ActionRepository
from services.actions_service import ActionService
from schemas.action_schema import ActionRequest, ActionResponse
from persistence.repositories.patient_registry_repository import (
    PatientRegistryRepository,
)
from services.patient_registry_service import PatientRegistryService
from persistence.repositories.vital_signs_repository import VitalSignsRepository
from services.vital_signs_service import VitalSignsService
from services.user_patient_service import UserPatientsService
from persistence.repositories.user_patient_repository import UserPatientsRepository
from persistence.repositories.patient_repository import PatientRepository
from services.patient_service import PatientService
from persistence.database import get_db
from schemas.patient_schema import (
    PatientRegistryRequest,
    PatientRegistryResponse,
    PatientRequest,
    PatientResponse,
    PatientUpdateRequest,
    PatientVitalSignsRequest,
    PatientVitalSignsResponse,
    UserPatientRequest,
    UserPatientResponse,
)


oncology_router = APIRouter(prefix="/oncology", tags=["oncology"])


@oncology_router.post("/patient/", response_model=PatientResponse)
@validate_route_permission
def add_patient(
    request: Request,
    patient: PatientRequest,
    db: Session = Depends(get_db),
    validated=Depends(validate_login),
    route_permission: str = "APT",
):
    try:
        patient = PatientService(PatientRepository(db)).create_patient(patient)

        UserPatientsService(
            userpatients_repository=UserPatientsRepository(db),
            user_repository=UserRepository(db),
        ).assign_patient_to_user(
            UserPatientRequest(user_id=request.state.user.id, patient_id=patient.id)
        )
    except ValueError as e:
        raise HTTPException(detail=str(e), status_code=400)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=500)
    return patient


@oncology_router.put("/patient/", response_model=PatientResponse)
def update_patient(
    request: Request,
    patient: PatientUpdateRequest,
    db: Session = Depends(get_db),
    validated=Depends(validate_login),
    route_permission: str = "UPT",
):
    try:
        patients_from_user = (
            UserPatientsService(
                userpatients_repository=UserPatientsRepository(db),
                user_repository=UserRepository(db),
            )
            .retrieve_user_patients(request.state.user.id)
            .patients
        )

        user_has_patient = patient.id in list(map(lambda x: x.id, patients_from_user))

        if not (user_has_patient):
            raise HTTPException(detail=str("Sin permisos."), status_code=403)

        patient = PatientService(PatientRepository(db)).update_patient(patient)
    except ValueError as e:
        raise HTTPException(detail=str(e), status_code=400)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=500)
    return patient


@oncology_router.get("/user/patient/", response_model=UserResponse)
def get_user_patients(
    user_id: int,
    db: Session = Depends(get_db),
    validated=Depends(validate_login),
    route_permission: str = "GUP",
):
    try:
        user_patients = UserPatientsService(
            userpatients_repository=UserPatientsRepository(db),
            user_repository=UserRepository(db),
        ).retrieve_user_patients(user_id)
    except ValueError as e:
        raise HTTPException(detail=str(e), status_code=400)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=500)
    return user_patients


@oncology_router.post("/user/patient/", response_model=UserPatientResponse)
def assign_patient_to_user(
    request: Request,
    user_patient: UserPatientRequest,
    db: Session = Depends(get_db),
    validated=Depends(validate_login),
    route_permission: str = "ANU",
):
    try:
        patients_from_user = (
            UserPatientsService(
                userpatients_repository=UserPatientsRepository(db),
                user_repository=UserRepository(db),
            )
            .retrieve_user_patients(request.state.user.id)
            .patients
        )

        user_has_patient = user_patient.patient_id in list(
            map(lambda x: x.id, patients_from_user)
        )

        if not (user_has_patient):
            raise HTTPException(detail=str("Sin permisos."), status_code=403)

        patients = UserPatientsService(
            userpatients_repository=UserPatientsRepository(db),
            user_repository=UserRepository(db),
        ).assign_patient_to_user(user_patient)
    except ValueError as e:
        raise HTTPException(detail=str(e), status_code=400)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=500)
    return patients


@oncology_router.get(
    "/patient/vitalsigns/", response_model=list[PatientVitalSignsResponse]
)
def get_vital_signs(
    request: Request,
    patient_id: int,
    db: Session = Depends(get_db),
    validated=Depends(validate_login),
    route_permission: str = "GVS",
):
    try:
        patients_from_user = (
            UserPatientsService(
                userpatients_repository=UserPatientsRepository(db),
                user_repository=UserRepository(db),
            )
            .retrieve_user_patients(request.state.user.id)
            .patients
        )

        user_has_patient = patient_id in list(map(lambda x: x.id, patients_from_user))

        if not (user_has_patient):
            raise HTTPException(detail=str("Sin permisos."), status_code=403)

        vital_signs = VitalSignsService(
            VitalSignsRepository(db), patient_repository=PatientRepository(db)
        ).get_vital_signs(patient_id)

        vital_signs.info = list(map(lambda x: x.__dict__, vital_signs.info))
    except ValueError as e:
        raise HTTPException(detail=str(e), status_code=400)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=500)
    return vital_signs


@oncology_router.post("/patient/vitalsigns/", response_model=PatientVitalSignsResponse)
def register_vital_signs(
    request: Request,
    vital_signs: PatientVitalSignsRequest,
    db: Session = Depends(get_db),
    validated=Depends(validate_login),
    route_permission: str = "RVS",
):
    try:
        patients_from_user = (
            UserPatientsService(
                userpatients_repository=UserPatientsRepository(db),
                user_repository=UserRepository(db),
            )
            .retrieve_user_patients(request.state.user.id)
            .patients
        )

        user_has_patient = vital_signs.patient_id in list(
            map(lambda x: x.id, patients_from_user)
        )

        if not (user_has_patient):
            raise HTTPException(detail=str("Sin permisos."), status_code=403)

        vital_signs = VitalSignsService(
            VitalSignsRepository(db), patient_repository=PatientRepository(db)
        ).register_vital_signs(vital_signs)

        vital_signs.info = list(map(lambda x: x.__dict__, vital_signs.info))

    except ValueError as e:
        raise HTTPException(detail=str(e), status_code=400)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=500)
    return vital_signs


@oncology_router.post("/patient/action/", response_model=PatientRegistryResponse)
def register_action(
    request: Request,
    patient_registry: PatientRegistryRequest,
    db: Session = Depends(get_db),
    validated=Depends(validate_login),
    route_permission: str = "RAU",
):
    try:
        patients_from_user = (
            UserPatientsService(
                userpatients_repository=UserPatientsRepository(db),
                user_repository=UserRepository(db),
            )
            .retrieve_user_patients(request.state.user.id)
            .patients
        )

        user_has_patient = patient_registry.patient_id in list(
            map(lambda x: x.id, patients_from_user)
        )

        if not (user_has_patient):
            raise HTTPException(detail=str("Sin permisos."), status_code=403)

        patient_registry_response = PatientRegistryService(
            PatientRegistryRepository(db)
        ).register_action(patient_registry)
    except ValueError as e:
        raise HTTPException(detail=str(e), status_code=400)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=500)
    return patient_registry_response


@oncology_router.get("/patient/action/", response_model=list[PatientRegistryResponse])
def get_patient_registry(
    request: Request,
    patient_id: int,
    db: Session = Depends(get_db),
    validated=Depends(validate_login),
    route_permission: str = "GPR",
):
    try:
        patients_from_user = (
            UserPatientsService(
                userpatients_repository=UserPatientsRepository(db),
                user_repository=UserRepository(db),
            )
            .retrieve_user_patients(request.state.user.id)
            .patients
        )

        user_has_patient = patient_id in list(map(lambda x: x.id, patients_from_user))

        if not (user_has_patient):
            raise HTTPException(detail=str("Sin permisos."), status_code=403)

        patient_registry = PatientRegistryService(
            PatientRegistryRepository(db)
        ).get_patient_registry(patient_id)
    except ValueError as e:
        raise HTTPException(detail=str(e), status_code=400)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=500)
    return patient_registry


@oncology_router.get("/action/", response_model=list[ActionResponse])
def get_actions(db: Session = Depends(get_db), route_permission: str = "GAC"):
    try:
        actions = ActionService(ActionRepository(db)).get_actions()
    except ValueError as e:
        raise HTTPException(detail=str(e), status_code=400)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=500)
    return actions


@oncology_router.post("/action/", response_model=ActionResponse)
def create_action(
    action: ActionRequest,
    db: Session = Depends(get_db),
    validated=Depends(validate_login),
    route_permission: str = "CAC",
):
    try:
        action_response = ActionService(ActionRepository(db)).create_action(action)
    except ValueError as e:
        raise HTTPException(detail=str(e), status_code=400)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=500)
    return action_response
