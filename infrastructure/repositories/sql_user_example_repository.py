
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from domain.models.user_example import UserExample
from domain.repositories.user_example_repository import UserExampleRepository
from infrastructure.persistence.entities.user_vocabulary import UserVocabularyModel
from infrastructure.persistence.entities.word_sense import WordSenseModel
from infrastructure.persistence.mappers.user_example_mapper import UserExampleMapper


class SQLUserExampleRepository(UserExampleRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_user_vocabulary_id(self, user_id: int, word_sense_id: int) -> int | None:
        stmt = (
            select(UserVocabularyModel.id)
            .join(
                WordSenseModel,
                WordSenseModel.word_id == UserVocabularyModel.vocabulary_word_id,
            )
            .where(
                UserVocabularyModel.user_id == user_id,
                WordSenseModel.id == word_sense_id,
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def save_all(self, user_examples: list[UserExample]) -> list[UserExample]:
        models = [UserExampleMapper.to_model(ex) for ex in user_examples]
        self.session.add_all(models)
        await self.session.commit()
        for model in models:
            await self.session.refresh(model)
        return [UserExampleMapper.to_entity(model) for model in models]
    
