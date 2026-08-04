from sqlalchemy import (
    Column, Integer, ForeignKey, Text
)
from sqlalchemy.orm import relationship
from database import Base

class UserExampleModel(Base):
    __tablename__ = "user_examples"

    id = Column(Integer, primary_key=True)

    sentence = Column(Text, nullable=False)

    word_sense_id = Column(
        Integer,
        ForeignKey("word_senses.id")
    )

    word_sense = relationship(
        "WordSenseModel",
        back_populates="user_examples"
    )
