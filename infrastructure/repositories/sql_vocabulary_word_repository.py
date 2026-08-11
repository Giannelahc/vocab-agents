
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from domain.models.vocabulary_word import VocabularyWord
from domain.repositories.vocabulary_word_repository import VocabularyWordRepository
from infrastructure.persistence.entities.vocabulary_word import VocabularyWordModel
from infrastructure.persistence.entities.user_vocabulary import UserVocabularyModel
from infrastructure.persistence.entities.word_sense import WordSenseModel
from infrastructure.persistence.mappers.vocabulary_word_mapper import VocabularyWordMapper
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


    async def find_by_word_and_language(self, word: str, language_id: int) -> VocabularyWord | None:

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
                    VocabularyWordModel.word == word,
                    VocabularyWordModel.language_id == language_id
                ))

        result = await self.session.execute(stmt)

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return VocabularyWordMapper.to_entity(model)

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

    async def find_by_user_id(self, user_id: int, language_id: int, page: int, page_size: int) -> list[VocabularyWord]:
        stmt = (select(VocabularyWordModel)
                .join(UserVocabularyModel)
                .options(
                    selectinload(VocabularyWordModel.language),
                    selectinload(VocabularyWordModel.senses)
                        .selectinload(WordSenseModel.examples),

                    selectinload(VocabularyWordModel.senses)
                        .selectinload(WordSenseModel.synonyms),

                    selectinload(VocabularyWordModel.senses)
                        .selectinload(WordSenseModel.user_examples), 
                )
                .order_by(VocabularyWordModel.created_at.desc())
                .offset((page - 1) * page_size)
                .limit(page_size)
                .where(UserVocabularyModel.user_id == user_id)
                )

        if language_id is not None:
            stmt = stmt.where(
                VocabularyWordModel.language_id == language_id
            )

        result = await self.session.execute(stmt)

        models = result.scalars().all()

        return [VocabularyWordMapper.to_entity(model) for model in models]