
from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, autoincrement=True)
    word        = Column(String(255), nullable=False)
    language_id = Column(
        Integer,
        ForeignKey("languages.id")
    )
    user_id = Column(Integer, ForeignKey("users.id"))

    language = relationship("Language")
    ##language      = Column(String(20), nullable=False)
    ##first_grammar_spec = Column(Text)
    ##second_grammar_spec = Column(Text)
    
    created_at    = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )