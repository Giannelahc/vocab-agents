#domain/models/user_vocabulary.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
    
@dataclass
class UserVocabulary:

    user_id: int
    vocabulary_word_id: int
    next_review_at: datetime

    created_at: Optional[datetime] = None

    id: Optional[int] = None
    last_review_at: Optional[datetime] = None

    learned: bool = False
    favorite: bool = False
    review_level: int = 0

    