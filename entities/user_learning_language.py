from sqlalchemy import (
    Column, Integer, ForeignKey
)
from sqlalchemy.orm import relationship
from database import Base

class UserLearningLanguageModel(Base):
    __tablename__ = "user_learning_languages"
    id = Column(Integer, primary_key=True, autoincrement=True)

    preference_id = Column(
        Integer,
        ForeignKey("user_preferences.id")
    )

    language_id = Column(
        Integer,
        ForeignKey("languages.id")
    )

    preference = relationship(
        "UserPreferenceModel",
        back_populates="learning_languages"
    )

    language = relationship("LanguageModel")