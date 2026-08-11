
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from domain.models.review import Review
from domain.repositories.review_repository import ReviewRepository
from infrastructure.persistence.entities.review import ReviewModel
from infrastructure.persistence.mappers.review_mapper import ReviewMapper
from infrastructure.persistence.enums.review_status import ReviewStatus as PersistenceReviewStatus
from application.enums.review_status import ReviewStatus


class SQLReviewRepository(ReviewRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, review: Review) -> Review:
        model = ReviewMapper.to_model(review)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        review.id = model.id
        return review

    async def update_status(self, review_id: int, status: ReviewStatus) -> None:
        stmt = select(ReviewModel).where(ReviewModel.id == review_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            raise ValueError(f"Vocabulary word with id {review_id} not found.")

        model.status = PersistenceReviewStatus(status.value)
        await self.session.flush()

