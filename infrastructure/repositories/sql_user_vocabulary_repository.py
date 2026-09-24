
from datetime import datetime, time, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from core.config import settings
from domain.models.user_vocabulary import UserVocabulary
from domain.models.flashcard_statistics import FlashcardStatistics
from domain.models.vocabulary_statistics import VocabularyStatistics
from domain.repositories.user_vocabulary_repository import UserVocabularyRepository
from infrastructure.persistence.entities.user_vocabulary import UserVocabularyModel
from infrastructure.persistence.entities.vocabulary_word import VocabularyWordModel
from infrastructure.persistence.entities.language import LanguageModel
from infrastructure.persistence.mappers.user_vocabulary_mapper import UserVocabularyMapper


class SQLUserVocabularyRepository(UserVocabularyRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user_vocabulary: UserVocabulary) -> UserVocabulary:
        model = UserVocabularyMapper.to_model(user_vocabulary)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return UserVocabularyMapper.to_entity(model)

    async def update(self, user_vocabulary: UserVocabulary) -> UserVocabulary:
        stmt = select(UserVocabularyModel).where(UserVocabularyModel.id == user_vocabulary.id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            raise ValueError(f"Vocabulary word with id {user_vocabulary.id} not found.")

        model.review_level=user_vocabulary.review_level
        model.fsrs_card=user_vocabulary.fsrs_card
        model.next_review_at=user_vocabulary.next_review_at
        await self.session.flush()
        await self.session.refresh(model)
        return UserVocabularyMapper.to_entity(model)

    async def find(self, user_id: int, vocabulary_word_id: int) -> UserVocabulary | None:
        stmt = select(UserVocabularyModel).where(
            UserVocabularyModel.user_id == user_id,
            UserVocabularyModel.vocabulary_word_id == vocabulary_word_id
        )

        result = await self.session.execute(stmt)

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return UserVocabularyMapper.to_entity(model)

    async def find_by_id(self, user_vocabulary_id: int) -> UserVocabulary | None:
        stmt = select(UserVocabularyModel).where(
            UserVocabularyModel.id == user_vocabulary_id
        )

        result = await self.session.execute(stmt)

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return UserVocabularyMapper.to_entity(model)


    async def get_vocabulary_statistics(
        self,
        user_id: int
    ) -> list[VocabularyStatistics]:
        now = datetime.now(timezone.utc)
        monday_date = now.date() - timedelta(days=now.weekday())
        week_start = datetime.combine(monday_date, time.min, tzinfo=timezone.utc)
        week_end = week_start + timedelta(days=7)

        learned_words = func.count(UserVocabularyModel.id).filter(
            UserVocabularyModel.review_level == settings.LEVEL_TO_FLASHCARDS
        )
        new_words_current_week = func.count(UserVocabularyModel.id).filter(
            UserVocabularyModel.created_at >= week_start,
            UserVocabularyModel.created_at < week_end,
        )

        stmt = (
            select(
                VocabularyWordModel.language_id,
                LanguageModel.name,
                learned_words.label("learned_words"),
                func.count(UserVocabularyModel.id).label("total_words"),
                new_words_current_week.label("new_words_current_week"),
            )
            .join(
                VocabularyWordModel,
                UserVocabularyModel.vocabulary_word_id == VocabularyWordModel.id,
            )
            .join(
                LanguageModel,
                VocabularyWordModel.language_id == LanguageModel.id,
            )
            .where(UserVocabularyModel.user_id == user_id)
            .group_by(VocabularyWordModel.language_id, LanguageModel.name)
            .order_by(VocabularyWordModel.language_id)
        )

        result = await self.session.execute(stmt)

        return [
            VocabularyStatistics(
                language_id=language_id,
                language_name=language_name,
                learned_words=learned_words_count or 0,
                total_words=total_words or 0,
                new_words_current_week=new_words_count or 0,
            )
            for (
                language_id,
                language_name,
                learned_words_count,
                total_words,
                new_words_count,
            ) in result.all()
        ]

    async def get_flashcards_statistics(self, user_id: int) -> FlashcardStatistics:

            local_tz = timezone(timedelta(hours=2))
            now = datetime.now(local_tz)

            start_of_today = now.replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0
            )
            end_of_today = start_of_today + timedelta(days=1)
            
            flashcards_to_review_stmt = (
                select(func.count(UserVocabularyModel.id))
                .where(
                    UserVocabularyModel.user_id == user_id,
                    UserVocabularyModel.review_level == settings.LEVEL_TO_FLASHCARDS,
                    UserVocabularyModel.next_review_at >= start_of_today,
                    UserVocabularyModel.next_review_at < end_of_today,
                )
            )

            flashcards_active = (
                select(func.count(UserVocabularyModel.id))
                .where(
                    UserVocabularyModel.user_id == user_id,
                    UserVocabularyModel.review_level == settings.LEVEL_TO_FLASHCARDS
                )
            )
    
            overdue_flashcards_stmt = (
                select(func.count(UserVocabularyModel.id))
                .where(
                    UserVocabularyModel.user_id == user_id,
                    UserVocabularyModel.review_level == settings.LEVEL_TO_FLASHCARDS,
                    UserVocabularyModel.next_review_at < start_of_today,
                )
            )

            flashcards_to_review = (await self.session.execute(flashcards_to_review_stmt)).scalar_one() or 0
            overdue_flashcards = (await self.session.execute(overdue_flashcards_stmt)).scalar_one() or 0
            flashcards_active_count = (await self.session.execute(flashcards_active)).scalar_one() or 0

            return FlashcardStatistics(
                flashcards_to_review=flashcards_to_review,
                overdue_flashcards=overdue_flashcards,
                flashcards_active=flashcards_active_count > 0
            )