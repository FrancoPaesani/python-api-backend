from datetime import datetime
from functools import wraps
from typing import Optional
from fastapi import Cookie, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from persistence.repositories.permission_repository import PermissionRepository
from domain.user import User
from persistence.repositories.user_repository import UserRepository
from services.auth_service import AuthService
from services.user_service import UserService
from persistence.database import get_db


def validate_login(
    request: Request,
    session_oncology_tkn_ath: Optional[str] = Cookie(None),
    db: Session = Depends(get_db),
):
    if session_oncology_tkn_ath is None:
        raise HTTPException(status_code=403, detail="Sesión inválida")

    session_db = AuthService(
        user_repository=UserRepository(db),
        permissions_repository=PermissionRepository(db),
    ).get_user_session(session_oncology_tkn_ath)

    if session_db is None:
        raise HTTPException(status_code=403, detail="Sesión inválida")

    if datetime.now() > session_db.expiry_date:
        raise HTTPException(status_code=403, detail="La sesión ha expirado")

    user: User = UserService(
        user_repository=UserRepository(db),
        permissions_repository=PermissionRepository(db),
    ).get_user_with_permissions_by_id(session_db.user_id)

    request.state.user = user


def validate_route_permission(func):
    @wraps(func)
    def wrapper(request: Request, route_permission: str, db: Session, *args, **kwargs):
        user_id = request.state.user.id
        user: User = UserService(
            user_repository=UserRepository(db),
            permissions_repository=PermissionRepository(db),
        ).get_user_with_permissions_by_id(user_id)
        permissions = list(map(lambda x: x.code, user.permissions))
        if route_permission in permissions:
            return func(request, db=db, *args, **kwargs)
        raise HTTPException(detail="Sin permisos.", status_code=403)

    return wrapper
