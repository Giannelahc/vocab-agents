
from sqlalchemy.ext.asyncio import AsyncSession

from domain.models.user_example import UserExample
from domain.repositories.user_example_repository import UserExampleRepository
from infrastructure.persistence.mappers.user_example_mapper import UserExampleMapper


class SQLUserExampleRepository(UserExampleRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_all(self, user_examples: list[UserExample]) -> list[UserExample]:
        models = [UserExampleMapper.to_model(ex) for ex in user_examples]
        self.session.add_all(models)
        await self.session.commit()
        for model in models:
            await self.session.refresh(model)
        return [UserExampleMapper.to_entity(model) for model in models]
    
