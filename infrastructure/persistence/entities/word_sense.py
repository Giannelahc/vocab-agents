
from sqlalchemy import (
    Column, Integer, DateTime, ForeignKey, String
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from infrastructure.persistence.database import Base

class WordSenseModel(Base):
    __tablename__ = "word_senses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    grammar_type = Column(String(30), nullable=False)
    definition = Column(JSONB, nullable=False)

    translations = Column(JSONB, nullable=True)
    gender = Column(JSONB, nullable=True)
    conjugation = Column(JSONB, nullable=True)

    word_id = Column(
        Integer,
        ForeignKey("words.id")
    )

    word = relationship("VocabularyWordModel", back_populates="senses")

    examples = relationship(
        "ExampleModel",
        back_populates="word_sense",
        cascade="all, delete-orphan"
    )

    user_examples = relationship(
        "UserExampleModel",
        back_populates="word_sense",
        cascade="all, delete-orphan"
    )

    synonyms = relationship(
        "SynonymModel",
        back_populates="word_sense",
        cascade="all, delete-orphan"
    )
    
    created_at    = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )