
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from datetime import datetime, timezone

from domain.models.review import Review
from domain.repositories.review_repository import ReviewRepository
from infrastructure.persistence.entities.review import ReviewModel
from infrastructure.persistence.entities.user_vocabulary import UserVocabularyModel
from infrastructure.persistence.mappers.review_mapper import ReviewMapper
from infrastructure.persistence.mappers.exercise_mapper import ExerciseMapper
from infrastructure.persistence.enums.review_status import ReviewStatus as PersistenceReviewStatus
from infrastructure.persistence.enums.generation_status import GenerationStatus as PersistenceGenerationStatus
from application.enums.review_status import ReviewStatus
from application.enums.generation_status import GenerationStatus


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

    async def get_reviews(self, user_id: int, status: ReviewStatus, up_to_now: bool) -> list[Review]:
        stmt = (select(ReviewModel)
                .join(UserVocabularyModel)
                .options(selectinload(ReviewModel.exercises))
                .where(UserVocabularyModel.user_id == user_id))
        
        if up_to_now:
            stmt = stmt.where(UserVocabularyModel.next_review_at <= datetime.now(timezone.utc))

        if status:
            stmt = stmt.where(ReviewModel.status == PersistenceReviewStatus(status.value))

        result = await self.session.execute(stmt)
        
        models = result.scalars().all()

        return [ReviewMapper.to_entity(model) for model in models]

    async def get_failed_reviews(self, user_id: int) -> list[Review]:
        stmt = (select(ReviewModel)
                .join(UserVocabularyModel)
                .options(selectinload(ReviewModel.exercises))
                .where(UserVocabularyModel.user_id == user_id,
                       ReviewModel.generation_status.in_([
                            PersistenceGenerationStatus.TO_GENERATE,
                            PersistenceGenerationStatus.FAILED
                        ]))
                )
        result = await self.session.execute(stmt)
                
        models = result.scalars().all()

        return [ReviewMapper.to_entity(model) for model in models]

    async def update_exercises(self, review: Review) -> None:
        stmt = (select(ReviewModel)
                .options(selectinload(ReviewModel.exercises))
                .where(ReviewModel.id == review.id))
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            raise ValueError(f"Review with id {review.id} not found.")

        model.generation_status = PersistenceGenerationStatus(review.generation_status.value)
        model.exercises = [
                    ExerciseMapper.to_model(exercise)
                    for exercise in review.exercises
                ]
        await self.session.flush()

    async def update_status(self, review_id: int, status: ReviewStatus) -> None:
        stmt = select(ReviewModel).where(ReviewModel.id == review_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            raise ValueError(f"Review with id {review_id} not found.")

        model.status = PersistenceReviewStatus(status.value)
        model.completed_at = datetime.now(timezone.utc)
        await self.session.flush()

    async def update_generation_status(self, review_id: int, status: GenerationStatus) -> None:
        stmt = select(ReviewModel).where(ReviewModel.id == review_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            raise ValueError(f"Review with id {review_id} not found.")

        model.generation_status = PersistenceGenerationStatus(status.value)
        await self.session.flush()

    async def find_by_id(self, review_id: int) -> Review:
        stmt = (select(ReviewModel)
                .options(selectinload(ReviewModel.exercises))
                .where(ReviewModel.id == review_id)
                )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return ReviewMapper.to_entity(model)



