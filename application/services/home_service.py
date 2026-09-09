import asyncio

from domain.models.home_info import HomeInfo
from domain.repositories.user_preference_repository import UserPreferenceRepository
from domain.repositories.user_repository import UserRepository
from domain.repositories.user_vocabulary_repository import UserVocabularyRepository

class HomeService:
    def __init__(self, user_repository: UserRepository,
                 user_vocabulary_repository: UserVocabularyRepository):
        self.user_repository = user_repository
        self.user_vocabulary_repository = user_vocabulary_repository

    async def get_home_summary(self, user_id) -> HomeInfo:
        user = await self.user_repository.find_by_id(user_id)

        new_words_current_week_task = self.user_vocabulary_repository.find_new_words_current_week()
        learned_words_task = self.user_vocabulary_repository.count_words_by_review_level_6()

        new_words_current_week, learned_words = await asyncio.gather(
            new_words_current_week_task,
            learned_words_task,
        )

        return HomeInfo(
            user.id,
            user.name,
            user.lastname,
            user.username,
            new_words_current_week,
            learned_words,
        )

