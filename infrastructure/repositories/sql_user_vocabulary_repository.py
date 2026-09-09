
from datetime import datetime, time, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from domain.models.user_vocabulary import UserVocabulary
from domain.models.vocabulary_word import VocabularyWord
from domain.repositories.user_vocabulary_repository import UserVocabularyRepository
from infrastructure.persistence.entities.user_vocabulary import UserVocabularyModel
from infrastructure.persistence.entities.vocabulary_word import VocabularyWordModel
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

    async def find_new_words_current_week(self) -> int:
        now = datetime.now(timezone.utc)
        monday_date = now.date() - timedelta(days=now.weekday())
        week_start = datetime.combine(monday_date, time.min, tzinfo=timezone.utc)
        week_end = week_start + timedelta(days=7)

        stmt = (
            select(func.count())
            .select_from(UserVocabularyModel)
            .where(
                UserVocabularyModel.created_at >= week_start,
                UserVocabularyModel.created_at < week_end,
            )
        )

        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def count_words_by_review_level_6(self) -> int:
        stmt = (
            select(func.count())
            .select_from(UserVocabularyModel)
            .where(UserVocabularyModel.review_level == 6)
        )

        result = await self.session.execute(stmt)
        return result.scalar_one()

    