from dataclasses import dataclass
from datetime import datetime


@dataclass
class ReviewHistory:
    id: int | None
    user_vocabulary_id: int
    rating: int
    reviewed_at: datetime
    scheduled_days: int