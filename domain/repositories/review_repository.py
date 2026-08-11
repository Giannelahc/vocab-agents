
from abc import ABC, abstractmethod

from application.enums.review_status import ReviewStatus
from domain.models.review import Review


class ReviewRepository(ABC):

    @abstractmethod
    async def save(self, review: Review) -> Review:
        pass

    @abstractmethod
    async def update_status(self, review_id: int, status: ReviewStatus) -> None:
        pass    

