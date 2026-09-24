
from sqlalchemy.ext.asyncio import AsyncSession

from domain.models.review_history import ReviewHistory
from domain.repositories.review_history_repository import ReviewHistoryRepository
from infrastructure.persistence.mappers.review_history_mapper import ReviewHistoryMapper


class SQLReviewRepository(ReviewHistoryRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, review_history: ReviewHistory) -> ReviewHistory:
        model = ReviewHistoryMapper.to_model(review_history)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        review_history.id = model.id
        return review_history
