from fastapi import HTTPException
from domain.models.user_preference import UserPreference
from domain.repositories.user_preference_repository import UserPreferenceRepository

class UserPreferenceService:
    def __init__(self,  user_preference_repository: UserPreferenceRepository):
        self.user_preference_repository = user_preference_repository

    async def get_user_preferences(self, user_id):
        return await self.user_preference_repository.find_by_user_id(user_id)

    async def save_user_preferences(self, user_preference: UserPreference):
        existing = await self.user_preference_repository.find_by_user_id(user_preference.user_id)
        if existing is not None:
            raise HTTPException(
                status_code=409,
                detail="User preference already exists for this user."
            )
        return await self.user_preference_repository.save(user_preference)
