
from abc import ABC, abstractmethod

from domain.models.review_history import ReviewHistory


class ReviewHistoryRepository(ABC):

    @abstractmethod
    async def create(self, review_history: ReviewHistory) -> ReviewHistory:
        pass
