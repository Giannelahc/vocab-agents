#domain/models/user_info.py
from dataclasses import dataclass
from domain.models.vocabulary_statistics import VocabularyStatistics

@dataclass
class HomeInfo:

    id: int
    name: str
    lastname: str
    username: str
    language_statistics: list[VocabularyStatistics]
    streak: int
    today_reviews: int
    flashcards_active: bool
    flashcards_to_review: int