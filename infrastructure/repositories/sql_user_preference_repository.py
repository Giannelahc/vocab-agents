
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from domain.models.user_preference import UserPreference
from domain.repositories.user_preference_repository import UserPreferenceRepository
from infrastructure.persistence.entities.user_learning_language import UserLearningLanguageModel
from infrastructure.persistence.entities.user_preferences import UserPreferenceModel
from infrastructure.persistence.mappers.language_mapper import LanguageMapper
from infrastructure.persistence.mappers.user_learning_language_mapper import UserLearningLanguageMapper
from infrastructure.persistence.mappers.user_preference_mapper import UserPreferenceMapper


class SQLUserPreferenceRepository(UserPreferenceRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user_preference: UserPreference) -> UserPreference:
        model = UserPreferenceMapper.to_model(user_preference)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return user_preference

    async def update(self, user_preference: UserPreference) -> UserPreference:
        stmt = (select(UserPreferenceModel)
                .options(
                        selectinload(UserPreferenceModel.learning_languages)
                            .selectinload(UserLearningLanguageModel.language)
                        )
                .where(UserPreferenceModel.id == user_preference.id))
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            raise ValueError(f"User preference with id {user_preference.id} not found.")

        model.user_id = user_preference.user_id
        model.native_language_id = user_preference.native_language_id

        model.learning_languages = [
            UserLearningLanguageMapper.to_model(language)
            for language in user_preference.learning_languages
        ]

        await self.session.commit()
        await self.session.refresh(model)
        return user_preference

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

    
