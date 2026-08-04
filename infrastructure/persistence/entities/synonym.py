from sqlalchemy import (
    Column, Integer, ForeignKey, String
)
from sqlalchemy.orm import relationship
from infrastructure.persistence.database import Base

class SynonymModel(Base):
    __tablename__ = "synonyms"

    id = Column(Integer, primary_key=True)

    word = Column(String(255), nullable=False)

    word_sense_id = Column(
        Integer,
        ForeignKey("word_senses.id")
    )

    word_sense = relationship(
        "WordSenseModel",
        back_populates="synonyms"
    )
