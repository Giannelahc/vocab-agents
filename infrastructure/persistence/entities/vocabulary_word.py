
from sqlalchemy import (
    Column, Enum, Integer, String, DateTime, ForeignKey
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from infrastructure.persistence.database import Base
from infrastructure.persistence.enums.vocabulary_status import VocabularyStatus

class VocabularyWordModel(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, autoincrement=True)
    word        = Column(String(255), nullable=False)
    status      = Column(Enum(VocabularyStatus), default=VocabularyStatus.PENDING, nullable=False)
    language_id = Column(
        Integer,
        ForeignKey("languages.id")
    )

    language = relationship("LanguageModel")

    senses = relationship(
        "WordSenseModel",
        back_populates="word",
        cascade="all, delete-orphan"
    )
    
    created_at    = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )