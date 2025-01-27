from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session

from persistence.repositories.permission_repository import PermissionRepository
from decorators.auth_decorators import validate_login
from persistence.database import get_db
from persistence.repositories.user_repository import UserRepository
from services.auth_service import AuthService
from schemas.management_schema import LoginUserRequest, LoginUserResponse


auth_router = APIRouter(prefix="/auth", tags=["AUTHENTICATION"])


@auth_router.post("/login/", response_model=LoginUserResponse)
def login_user(
    response: Response, credentials: LoginUserRequest, db: Session = Depends(get_db)
):
    try:
        user = AuthService(
            user_repository=UserRepository(db),
            permissions_repository=PermissionRepository(db),
        ).authenticate_user(credentials)
        response.set_cookie("session_oncology_tkn_ath", user.jwt_token)
    except ConnectionRefusedError as e:
        raise HTTPException(detail=str(e), status_code=403)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=500)
    return user


@auth_router.post("/logout/")
def logout_user(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
    validated=Depends(validate_login),
):
    try:
        logout_made = AuthService(
            user_repository=UserRepository(db),
            permissions_repository=PermissionRepository(db),
        ).logout_user(request.state.user.id)
        response.delete_cookie("session_oncology_tkn_ath")
    except ConnectionRefusedError as e:
        raise HTTPException(detail=str(e), status_code=403)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=500)
    return logout_made
