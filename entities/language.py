from sqlalchemy import (
    Column, Integer, ForeignKey, String
)
from sqlalchemy.sql import func
from database import Base

class Language(Base):
    __tablename__ = "languages"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    code = Column(String(5))