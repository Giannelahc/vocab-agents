from sqlalchemy import (
    Column, Integer, ForeignKey, Text
)
from sqlalchemy.orm import relationship
from infrastructure.persistence.database import Base

class UserExampleModel(Base):
    __tablename__ = "user_examples"

    id = Column(Integer, primary_key=True)

    sentence = Column(Text, nullable=False)

    user_vocabulary_id = Column(
        Integer,
        ForeignKey(
            "user_vocabularies.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    word_sense_id = Column(
        Integer,
        ForeignKey("word_senses.id")
    )

    user_vocabulary = relationship(
        "UserVocabularyModel",
        back_populates="user_examples"
    )

    word_sense = relationship(
        "WordSenseModel",
        back_populates="user_examples"
    )
