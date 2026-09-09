
from abc import ABC, abstractmethod

from application.enums.review_status import ReviewStatus
from application.enums.generation_status import GenerationStatus
from domain.models.review import Review
from domain.models.review_summary import ReviewSummary
from domain.models.review_statistics import ReviewStatistics


class ReviewRepository(ABC):

    @abstractmethod
    async def save(self, review: Review) -> Review:
        pass

    @abstractmethod
    async def get_reviews(self, user_id: int, status: ReviewStatus, up_to_now: bool, page: int = 1, page_size: int = 50) -> tuple[list[ReviewSummary], int]:
        pass

    @abstractmethod
    async def get_failed_reviews(self, user_id: int) -> list[Review]:
        pass

    @abstractmethod
    async def update_exercises(self, review: Review) -> Review:
        pass

    @abstractmethod
    async def update_status(self, review_id: int, status: ReviewStatus) -> None:
        pass   

    @abstractmethod
    async def update_generation_status(self, review_id: int, status: GenerationStatus) -> None:
        pass  

    @abstractmethod
    async def find_by_id(self, review_id) -> Review:
        pass 

    @abstractmethod
    async def find_by_user_vocabulary_id_and_status(self, user_vocabulary_id: int, status: ReviewStatus) -> Review:
        pass

    @abstractmethod
    async def get_statistics(self, user_id: int) -> ReviewStatistics:
        pass
