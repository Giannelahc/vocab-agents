#domain/models/user_info.py
from dataclasses import dataclass
from datetime import datetime
from domain.models.user_preference import UserPreference

@dataclass
class HomeInfo:

    id: int
    name: str
    lastname: str
    username: str
    newWordsCurrentWeek: int
    learnedWords: int