#domain/models/user_learning_language.py
from dataclasses import dataclass
from typing import Optional

from domain.models.language import Language
    
@dataclass
class UserLearningLanguage:

    language_id: int
    language: Language

    id: Optional[int] = None
    