from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from application.enums.review_status import ReviewStatus
from application.enums.generation_status import GenerationStatus

@dataclass
class ReviewNotificationSummary:

    today_reviews: int
    overdue_reviews: int
    total_pending: int