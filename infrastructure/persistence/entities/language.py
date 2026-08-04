from sqlalchemy import (
    Column, Integer, ForeignKey, String
)
from sqlalchemy.sql import func
from infrastructure.persistence.database import Base

class LanguageModel(Base):
    __tablename__ = "languages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(5))
    name = Column(String(20), nullable=False)