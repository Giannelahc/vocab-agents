from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from application.enums.review_status import ReviewStatus
from application.enums.generation_status import GenerationStatus

@dataclass
class ReviewSummary:

    user_vocabulary_id: int
    status: ReviewStatus
    generation_status: GenerationStatus
    word: str
    review_level: int
    next_review_at: datetime
    exercises: int = 0
    id: Optional[int] = None
    completed_at: Optional[datetime] = None

