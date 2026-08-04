from sqlalchemy import (
    Column, Integer, String, DateTime
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class UserModel(Base):
    __tablename__ = "users"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    name            = Column(String(20), nullable=False)
    lastname        = Column(String(20), nullable=False)
    username        = Column(String(20), nullable=False)
    email           = Column(String(120), nullable=False, unique=True)
    password_hash   = Column(String(255), nullable=False)
    preferences     = relationship(
        "UserPreferenceModel",
        back_populates="user",
        uselist=False
    )
    
    created_at    = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )