
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from domain.models.user_preference import UserPreference
from domain.repositories.user_preference_repository import UserPreferenceRepository
from infrastructure.persistence.entities.user_learning_language import UserLearningLanguageModel
from infrastructure.persistence.entities.user_preferences import UserPreferenceModel
from infrastructure.persistence.mappers.user_preference_mapper import UserPreferenceMapper


class SQLUserPreferenceRepository(UserPreferenceRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user_preference: UserPreference) -> UserPreference:
        model = UserPreferenceMapper.to_model(user_preference)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        user_preference.id = model.id
        return user_preference##UserPreferenceMapper.to_entity(model)


    async def find_by_user_id(self, user_id: int) -> UserPreference | None:

        stmt = (select(UserPreferenceModel)
        .options(
            selectinload(UserPreferenceModel.native_language),
            selectinload(UserPreferenceModel.learning_languages)
                .selectinload(UserLearningLanguageModel.language)
        )
        .where(
            UserPreferenceModel.user_id == user_id
        ))

        result = await self.session.execute(stmt)

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return UserPreferenceMapper.to_entity(model)

    
