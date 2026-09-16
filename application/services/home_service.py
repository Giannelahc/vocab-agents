import asyncio
from datetime import datetime

from domain.models.home_info import HomeInfo
from domain.repositories.review_repository import ReviewRepository
from domain.repositories.user_repository import UserRepository
from domain.repositories.user_vocabulary_repository import UserVocabularyRepository

class HomeService:
    def __init__(self, user_repository: UserRepository,
                 user_vocabulary_repository: UserVocabularyRepository,
                 review_repository: ReviewRepository):
        self.user_repository = user_repository
        self.user_vocabulary_repository = user_vocabulary_repository
        self.review_repository = review_repository

    async def get_home_summary(self, user_id) -> HomeInfo:
        user = await self.user_repository.find_by_id(user_id)

        vocabulary_statistics = await self.user_vocabulary_repository.get_vocabulary_statistics(user_id)

        statistics = await self.review_repository.get_statistics(user_id)
        if statistics.overdue_reviews > 0 and user.streak > 0:

            await self.user_repository.update_streak(
                user_id=user_id,
                streak=0
            )

            user.streak = 0


        return HomeInfo(
            user.id,
            user.name,
            user.lastname,
            user.username,
            vocabulary_statistics,
            user.streak,
            statistics.reviews_to_review
        )

