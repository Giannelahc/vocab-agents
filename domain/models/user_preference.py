#domain/models/user_preference.py
from dataclasses import dataclass, field
from typing import Optional
from domain.models.language import Language
from domain.models.user_learning_language import UserLearningLanguage
    
@dataclass
class UserPreference:

    id: Optional[int]
    user_id: int
    native_language_id: int
    native_language: Language
    
    learning_languages: list[UserLearningLanguage] = field(default_factory=list)