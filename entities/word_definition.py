
from sqlalchemy import (
    Column, Integer, Text, DateTime, ForeignKey
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class WordDefinition(Base):
    __tablename__ = "word_definitions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    word_id = Column(
        Integer,
        ForeignKey("words.id")
    )
    language_id = Column(
        Integer,
        ForeignKey("languages.id")
    )

    definition = Column(Text)

    language = relationship("Language")
    word = relationship("Word")
    
    created_at    = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )