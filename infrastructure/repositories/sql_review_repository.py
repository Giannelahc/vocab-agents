
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from datetime import datetime, timezone

from domain.models.review import Review
from domain.models.review_summary import ReviewSummary
from domain.models.review_statistics import ReviewStatistics
from domain.repositories.review_repository import ReviewRepository
from infrastructure.persistence.entities.review import ReviewModel
from infrastructure.persistence.entities.user_vocabulary import UserVocabularyModel
from infrastructure.persistence.entities.exercise import ExerciseModel
from infrastructure.persistence.entities.vocabulary_word import VocabularyWordModel
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

    async def get_reviews(
        self,
        user_id: int,
        status: ReviewStatus | None,
        up_to_now: bool,
        page: int = 1,
        page_size: int = 50
    ) -> tuple[list[ReviewSummary], int]:

        exercise_count = (
            select(func.count(ExerciseModel.id))
            .where(
                ExerciseModel.review_id == ReviewModel.id
            )
            .correlate(ReviewModel)
            .scalar_subquery()
        )

        base_conditions = [
            UserVocabularyModel.user_id == user_id
        ]

        if up_to_now:
            base_conditions.append(
                UserVocabularyModel.next_review_at
                <= datetime.now(timezone.utc)
            )

        if status:
            base_conditions.append(
                ReviewModel.status
                == PersistenceReviewStatus(status.value)
            )

        # Total
        count_stmt = (
            select(func.count(ReviewModel.id))
            .join(
                UserVocabularyModel,
                ReviewModel.user_vocabulary_id == UserVocabularyModel.id
            )
            .where(*base_conditions)
        )

        total = await self.session.scalar(count_stmt)

        # Items
        stmt = (
            select(
                ReviewModel,
                UserVocabularyModel.review_level,
                UserVocabularyModel.next_review_at,
                VocabularyWordModel.word,
                exercise_count.label("exercise_count")
            )
            .join(
                UserVocabularyModel,
                ReviewModel.user_vocabulary_id
                == UserVocabularyModel.id
            )
            .join(
                VocabularyWordModel,
                UserVocabularyModel.vocabulary_word_id
                == VocabularyWordModel.id
            )
            .where(*base_conditions)
            .order_by(
                UserVocabularyModel.next_review_at.asc()
            )
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        result = await self.session.execute(stmt)

        models = result.all()

        items = [
            ReviewMapper.to_summary_entity(
                review,
                word,
                review_level,
                next_review_at,
                exercise_count
            )
            for (
                review,
                review_level,
                next_review_at,
                word,
                exercise_count
            ) in models
        ]

        return items, total or 0

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

    async def find_by_id(self, review_id: int) -> Review | None:
        stmt = (select(ReviewModel)
                .options(selectinload(ReviewModel.exercises))
                .where(ReviewModel.id == review_id)
                )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return ReviewMapper.to_entity(model)

    async def find_by_user_vocabulary_id_and_status(self, user_vocabulary_id: int, status: ReviewStatus) -> Review | None:
        stmt = (select(ReviewModel)
                .options(selectinload(ReviewModel.exercises))
                .where(ReviewModel.user_vocabulary_id == user_vocabulary_id,
                       ReviewModel.status == PersistenceReviewStatus(status.value))
                )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return ReviewMapper.to_entity(model)

    async def get_statistics(self, user_id: int) -> ReviewStatistics:

        now = datetime.now(timezone.utc)

        start_of_today = now.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

        review_stats = (
            select(
                func.count(ReviewModel.id)
                    .filter(
                        ReviewModel.status == PersistenceReviewStatus.PASSED
                    )
                    .label("completed_reviews"),

                func.count(ReviewModel.id)
                    .filter(
                        ReviewModel.status == PersistenceReviewStatus.FAILED
                    )
                    .label("failed_reviews")
            )
                    .select_from(ReviewModel)
            .join(
                UserVocabularyModel,
                ReviewModel.user_vocabulary_id == UserVocabularyModel.id
            )
            .where(
                UserVocabularyModel.user_id == user_id
            )
            .subquery()
        )

        vocabulary_stats = (
            select(
                func.count(ReviewModel.id)
                    .filter(
                        UserVocabularyModel.next_review_at <= now
                    )
                    .label("reviews_to_review"),
                func.count(ReviewModel.id)
                    .filter(
                        UserVocabularyModel.next_review_at < start_of_today
                    )
                    .label("overdue_reviews")
            )
                    .select_from(ReviewModel)
            .join(
                UserVocabularyModel,
                ReviewModel.user_vocabulary_id == UserVocabularyModel.id
            )
            .where(
                UserVocabularyModel.user_id == user_id,
                ReviewModel.status == PersistenceReviewStatus.PENDING
            )
            .subquery()
        )

        stmt = select(
            review_stats.c.completed_reviews,
            review_stats.c.failed_reviews,
            vocabulary_stats.c.reviews_to_review,
            vocabulary_stats.c.overdue_reviews
        )

        result = await self.session.execute(stmt)

        row = result.one()

        completed_reviews = row.completed_reviews or 0
        failed_reviews = row.failed_reviews or 0

        total_finished_reviews = (
            completed_reviews + failed_reviews
        )

        success_rate = (
            completed_reviews / total_finished_reviews * 100
            if total_finished_reviews > 0
            else 0.0
        )

        return ReviewStatistics(
            success_rate=round(success_rate, 2),
            reviews_to_review=row.reviews_to_review or 0,
            overdue_reviews=row.overdue_reviews or 0
        )