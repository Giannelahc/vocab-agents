
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from domain.models.language import Language
from domain.repositories.language_repository import LanguageRepository
from infrastructure.persistence.entities.language import LanguageModel
from infrastructure.persistence.mappers.language_mapper import LanguageMapper


class SQLLanguageRepository(LanguageRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, language: Language) -> Language:
        model = LanguageMapper.to_model(language)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return LanguageMapper.to_entity(model)

    async def save_all(self, languages: list[LanguageModel]) -> list[LanguageModel]:
        models = [LanguageMapper.to_model(lang) for lang in languages]
        self.session.add_all(models)
        await self.session.commit()
        for model in models:
            await self.session.refresh(model)
        return [LanguageMapper.to_entity(model) for model in models]

    async def count(self) -> int:
        stmt = select(func.count()).select_from(LanguageModel)

        result = await self.session.execute(stmt)

        return result.scalar_one()
    

    async def find_by_id(self, language_id: int) -> Language | None:

        stmt = select(LanguageModel).where(
            LanguageModel.id == language_id
        )

        result = await self.session.execute(stmt)

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return LanguageMapper.to_entity(model)

    async def find_all(self) -> list[Language]:
        stmt = select(LanguageModel)

        result = await self.session.execute(stmt)

        model = result.scalars().all()
        return [LanguageMapper.to_entity(lang) for lang in model]
    
