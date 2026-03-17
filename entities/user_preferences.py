from sqlalchemy import (
    Column, Integer, ForeignKey
)
from sqlalchemy.orm import relationship
from database import Base

class UserPreference(Base):
    __tablename__ = "user_preferences"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    native_language_id = Column(
        Integer,
        ForeignKey("languages.id")
    )
    user = relationship("User", back_populates="preferences")
    native_language = relationship("Language")
    learning_languages = relationship(
        "UserLearningLanguage",
        back_populates="preference"
    )