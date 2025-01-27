from datetime import datetime
from sqlalchemy import Column, ForeignKey, Identity, Integer, String, Boolean, DateTime
from ..database import Base


class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, Identity(always=True), primary_key=True, index=True)
    code = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    active = Column(Boolean, default=True)
    date_created = Column(DateTime, nullable=False, default=datetime.now)


class PermissionsDB(Base):
    __tablename__ = "permissions"
    id = Column(Integer, Identity(always=True), primary_key=True, index=True)
    code = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    date_created = Column(DateTime, nullable=False, default=datetime.now)


class UserPermissionsDB(Base):
    __tablename__ = "user_permissions"
    user_id = Column(ForeignKey("users.id"), primary_key=True)
    permission_id = Column(ForeignKey("permissions.id"), primary_key=True)
    date_created = Column(DateTime, nullable=False, default=datetime.now)
    user_created = Column(ForeignKey("users.id"))
