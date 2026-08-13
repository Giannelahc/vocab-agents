
# application/services/review_scheduler.py

from datetime import datetime, timedelta, timezone
from core.config import settings


class ReviewScheduler:

    @staticmethod
    def schedule_next_review(level: int) -> datetime:
        index = min(level, len(settings.INTERVALS) - 1)
        days = settings.INTERVALS[index]
        return datetime.now(timezone.utc) + timedelta(days=days)

