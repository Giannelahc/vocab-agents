
from sqlalchemy import (
    Column, Integer, DateTime, ForeignKey
)
from sqlalchemy.sql import func
from database import Base

class UserVocabularyModel(Base):
    __tablename__ = "user_vocabularies"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    vocabulary_word_id = Column(Integer, ForeignKey("words.id"))

    favorite = Column(Integer, default=0)

    learned = Column(Integer, default=0)

    review_level = Column(Integer, default=0)

    next_review_at = Column(DateTime(timezone=True), nullable=False)

    last_review_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at    = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
