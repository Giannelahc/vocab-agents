# schemas/user.py
from pydantic import BaseModel
from datetime import datetime
from schemas.preference import UserPreferenceDto


class UserInfoResponse(BaseModel):
    id: int
    name: str
    lastname: str
    username: str
    email: str
    created_at: datetime
    preference: UserPreferenceDto | None = None

class VocabularyStatisticsDto(BaseModel):
    language_id: int
    language_name: str
    learned_words: int
    total_words: int
    new_words_current_week: int

class HomeInfoResponse(BaseModel):
    id: int
    name: str
    lastname: str
    username: str
    language_statistics: list[VocabularyStatisticsDto]
    streak: int
    today_reviews: int
    flashcards_active: bool
    flashcards_to_review: int