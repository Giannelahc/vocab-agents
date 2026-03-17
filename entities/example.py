from sqlalchemy import (
    Column, Integer, ForeignKey, Text
)
from sqlalchemy.sql import func
from database import Base

class Example(Base):
    __tablename__ = "example_sentences"

    id = Column(Integer, primary_key=True)

    word_id = Column(
        Integer,
        ForeignKey("words.id")
    )

    sentence = Column(Text)

    language_id = Column(
        Integer,
        ForeignKey("languages.id")
    )