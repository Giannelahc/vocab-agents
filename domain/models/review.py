#domain/models/review.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from application.enums.review_status import ReviewStatus
from application.enums.generation_status import GenerationStatus
from domain.models.exercise import Exercise
    
@dataclass
class Review:

    user_vocabulary_id: int
    status: ReviewStatus
    generation_status: GenerationStatus
    exercises: list[Exercise]
    id: Optional[int] = None
    completed_at: Optional[datetime] = None

    