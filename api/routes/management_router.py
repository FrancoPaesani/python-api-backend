from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from decorators.auth_decorators import validate_login
from services.management_service import ManagementService
from persistence.repositories.permission_repository import PermissionRepository
from schemas.management_schema import (
    PermissionRequest,
    PermissionResponse,
    UserRequest,
    UserResponse,
)
from persistence.database import get_db
from persistence.repositories.user_repository import UserRepository
from services.user_service import UserService

user_router = APIRouter(prefix="/management", tags=["USER MANAGEMENT"])


@user_router.post("/users/", response_model=UserResponse)
def create_user(
    user: UserRequest,
    db: Session = Depends(get_db),
    validated=Depends(validate_login),
    route_permission: str = "CUS",
):
    try:
        created_user = UserService(
            UserRepository(db), permissions_repository=PermissionRepository(db)
        ).create_user(user)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=500)
    return created_user


@user_router.post("/permissions/", response_model=PermissionResponse)
def create_permission(
    permission: PermissionRequest,
    db: Session = Depends(get_db),
    validated=Depends(validate_login),
    route_permission: str = "CPM",
):
    try:
        created_permission = ManagementService(
            PermissionRepository(db), UserRepository(db)
        ).create_permission(permission)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=500)
    return created_permission


@user_router.post("/users/permissions/")
def assign_permission_to_user(
    user_id: int,
    permission_id: int,
    db: Session = Depends(get_db),
    validated=Depends(validate_login),
    route_permission: str = "APU",
):
    try:
        user_permission = ManagementService(
            PermissionRepository(db), UserRepository(db)
        ).assign_permission(user_id, permission_id)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=500)
    return user_permission


@user_router.post("/users/enable/")
def enable_user(
    user_id: int,
    db: Session = Depends(get_db),
    validated=Depends(validate_login),
    route_permission: str = "EUS",
):
    try:
        user = UserService(
            UserRepository(db), permissions_repository=PermissionRepository(db)
        ).enable_user(user_id)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=500)
    return user


@user_router.post("/users/disable/")
def disable(
    user_id: int,
    db: Session = Depends(get_db),
    validated=Depends(validate_login),
    route_permission: str = "DUS",
):
    try:
        user = UserService(
            UserRepository(db), permissions_repository=PermissionRepository(db)
        ).disable_user(user_id)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=500)
    return user
