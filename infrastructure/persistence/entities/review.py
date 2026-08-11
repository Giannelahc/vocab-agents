
from sqlalchemy import (
    Column, Enum, Integer, String, DateTime, ForeignKey
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from infrastructure.persistence.database import Base
from infrastructure.persistence.enums.review_status import ReviewStatus

class ReviewModel(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_vocabulary_id = Column(Integer, ForeignKey("user_vocabularies.id"))
    status      = Column(Enum(ReviewStatus), default=ReviewStatus.PENDING, nullable=False)

    completed_at = Column(DateTime(timezone=True), nullable=True)

    exercises = relationship(
        "ExerciseModel",
        back_populates="review",
        cascade="all, delete-orphan"
    )

    created_at    = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )