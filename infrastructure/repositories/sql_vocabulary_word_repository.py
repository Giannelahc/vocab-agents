
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from domain.models.vocabulary_word import VocabularyWord
from domain.models.vocabulary_word_summary import VocabularyWordSummary
from domain.repositories.vocabulary_word_repository import VocabularyWordRepository
from infrastructure.persistence.entities.vocabulary_word import VocabularyWordModel
from infrastructure.persistence.entities.user_vocabulary import UserVocabularyModel
from infrastructure.persistence.entities.word_sense import WordSenseModel
from infrastructure.persistence.mappers.vocabulary_word_mapper import VocabularyWordMapper
from infrastructure.persistence.mappers.vocabulary_word_summary_mapper import VocabularyWordSummaryMapper
from infrastructure.persistence.enums.vocabulary_status import VocabularyStatus as PersistenceVocabularyStatus
from application.enums.vocabulary_status import VocabularyStatus
from infrastructure.persistence.mappers.word_sense_mapper import WordSenseMapper


class SQLVocabularyWordRepository(VocabularyWordRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, vocabulary_word: VocabularyWord) -> VocabularyWord:
        model = VocabularyWordMapper.to_model(vocabulary_word)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        vocabulary_word.id = model.id
        return vocabulary_word##VocabularyWordMapper.to_entity(model)

    async def update_status(self, vocabulary_word_id: int, status: VocabularyStatus) -> None:
        stmt = select(VocabularyWordModel).where(VocabularyWordModel.id == vocabulary_word_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            raise ValueError(f"Vocabulary word with id {vocabulary_word_id} not found.")

        model.status = PersistenceVocabularyStatus(status.value)
        await self.session.flush()

    async def update_senses(self, vocabulary_word: VocabularyWord) -> VocabularyWord:
        stmt = (select(VocabularyWordModel)
                .options(selectinload(VocabularyWordModel.senses))
                .where(VocabularyWordModel.id == vocabulary_word.id))
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            raise ValueError(f"Vocabulary word with id {vocabulary_word.id} not found.")

        model.status = PersistenceVocabularyStatus(vocabulary_word.status.value)

        # Update the senses
        model.senses = [
            WordSenseMapper.to_model(sense)
            for sense in vocabulary_word.senses
        ]

        await self.session.flush()
        await self.session.refresh(model)
        vocabulary_word.id = model.id
        return vocabulary_word##VocabularyWordMapper.to_entity(model)


    async def find_by_word_and_language(self, word: str, language_id: int) -> VocabularyWordSummary | None:

        sense_count = (
            select(func.count(WordSenseModel.id))
            .where(WordSenseModel.word_id == VocabularyWordModel.id)
            .correlate(VocabularyWordModel)
            .scalar_subquery()
        )

        stmt = (select(VocabularyWordModel, sense_count.label("sense_count"))
                .options(
                    selectinload(VocabularyWordModel.language)
                )
                .where( 
                    VocabularyWordModel.word == word,
                    VocabularyWordModel.language_id == language_id
                ))

        result = await self.session.execute(stmt)

        model = result.one_or_none()

        if model is None:
            return None

        return VocabularyWordSummaryMapper.to_entity(model, sense_count)

    async def find_by_id(self, vocabulary_word_id: int) -> VocabularyWord | None:
        stmt = (select(VocabularyWordModel)
                .options(
                    selectinload(VocabularyWordModel.language),
                    selectinload(VocabularyWordModel.senses)
                        .selectinload(WordSenseModel.examples),

                    selectinload(VocabularyWordModel.senses)
                        .selectinload(WordSenseModel.synonyms),

                    selectinload(VocabularyWordModel.senses)
                        .selectinload(WordSenseModel.user_examples), 
                )
                .where( 
                    VocabularyWordModel.id == vocabulary_word_id
                ))

        result = await self.session.execute(stmt)

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return VocabularyWordMapper.to_entity(model)

    async def find_by_user_id(self, user_id: int, language_id: int | None,
                              page: int, page_size: int, search: str) -> tuple[list[VocabularyWordSummary], int]:

        sense_count = (
            select(func.count(WordSenseModel.id))
            .where(WordSenseModel.word_id == VocabularyWordModel.id)
            .correlate(VocabularyWordModel)
            .scalar_subquery()
        )

        stmt = (
            select(VocabularyWordModel, sense_count.label("sense_count"))
            .join(UserVocabularyModel)
            .options(selectinload(VocabularyWordModel.language))
            .where(UserVocabularyModel.user_id == user_id)
            .order_by(VocabularyWordModel.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        count_stmt = (
            select(func.count(VocabularyWordModel.id))
            .join(UserVocabularyModel)
            .where(
                UserVocabularyModel.user_id == user_id
            )
        )

        if language_id is not None:
            stmt = stmt.where(
                VocabularyWordModel.language_id == language_id
            )

            count_stmt = count_stmt.where(
                VocabularyWordModel.language_id == language_id
            )

        if search:
            search_pattern = f"%{search.strip()}%"
            stmt = stmt.where(VocabularyWordModel.word.ilike(search_pattern))
            count_stmt = count_stmt.where(VocabularyWordModel.word.ilike(search_pattern))

        result = await self.session.execute(stmt)

        models = result.all()

        count_result = await self.session.execute(count_stmt)

        total = count_result.scalar_one()

        words = [
            VocabularyWordSummaryMapper.to_entity(model, sense_count)
            for model, sense_count in models
        ]

        return words, total
    

    async def find_existing_words(self, user_id: int, language_id: int, words: list[str]) -> set[str]:

        stmt = (
            select(VocabularyWordModel.word)
            .join(
                UserVocabularyModel,
                UserVocabularyModel.vocabulary_word_id
                == VocabularyWordModel.id
            )
            .where(
                UserVocabularyModel.user_id == user_id,
                VocabularyWordModel.language_id == language_id,
                VocabularyWordModel.word.in_(words)
            )
        )

        result = await self.session.execute(stmt)

        return {
            word.strip().lower()
            for word in result.scalars().all()
        }