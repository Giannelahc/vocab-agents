from sqlalchemy import (
    Column, Integer, ForeignKey
)
from sqlalchemy.orm import relationship
from database import Base

class UserPreferenceModel(Base):
    __tablename__ = "user_preferences"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    native_language_id = Column(
        Integer,
        ForeignKey("languages.id")
    )
    user = relationship("UserModel", back_populates="preferences")
    native_language = relationship("LanguageModel")
    learning_languages = relationship(
        "UserLearningLanguageModel",
        back_populates="preference"
    )