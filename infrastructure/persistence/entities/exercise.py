
from sqlalchemy import (
    Column, Integer, DateTime, ForeignKey, Text, String, Enum
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from infrastructure.persistence.database import Base
from infrastructure.persistence.enums.exercise_type import ExerciseType

class ExerciseModel(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, autoincrement=True)

    type = Column(Enum(ExerciseType), nullable=False)
    question = Column(Text, nullable=False)
    options = Column(JSONB, nullable=False)
    correct_answer = Column(Integer, nullable=False)

    review_id = Column(
        Integer,
        ForeignKey("reviews.id"),
        nullable=False
    )

    review = relationship("ReviewModel", back_populates="exercises")
    
    created_at    = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )