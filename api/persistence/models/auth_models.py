from datetime import datetime
from sqlalchemy import Column, ForeignKey, DateTime, Text
from ..database import Base


class UserSessionDB(Base):
    __tablename__ = "user_session"
    user_id = Column(ForeignKey("users.id"), primary_key=True)
    jwt_token = Column(Text)
    expiry_date = Column(DateTime, nullable=False)
    created = Column(DateTime, nullable=False, default=datetime.now)
