from domain.models.user_info import UserInfo
from domain.repositories.user_preference_repository import UserPreferenceRepository
from domain.repositories.user_repository import UserRepository

class UserService:
    def __init__(self,  user_preference_repository: UserPreferenceRepository,
                 user_repository: UserRepository):
        self.user_preference_repository = user_preference_repository
        self.user_repository = user_repository

    async def get_user_info(self, user_id) -> UserInfo:
        user = await self.user_repository.find_by_id(user_id)
        user_preference = await self.user_preference_repository.find_by_user_id(user_id)
        return UserInfo(user.id, user.name, user.lastname, user.username, user.email, user.created_at, user_preference)

