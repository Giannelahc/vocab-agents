
from sqlalchemy import (
    Column, Float, Integer, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship
from infrastructure.persistence.database import Base


class ReviewHistoryModel(Base):
    __tablename__ = "review_history"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    user_vocabulary_id = Column(
        Integer,
        ForeignKey(
            "user_vocabularies.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    rating = Column(
        Integer,
        nullable=False
    )

    reviewed_at = Column(
        DateTime(timezone=True),
        nullable=False
    )

    scheduled_days = Column(
        Float,
        nullable=False
    )

    user_vocabulary = relationship(
        "UserVocabularyModel",
        back_populates="review_history"
    )