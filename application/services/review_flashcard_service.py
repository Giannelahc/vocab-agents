

from datetime import date, datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from domain.repositories.review_history_repository import ReviewHistoryRepository
from domain.models.review_history import ReviewHistory
from domain.repositories.user_vocabulary_repository import UserVocabularyRepository
from domain.repositories.user_repository import UserRepository
from domain.repositories.review_repository import ReviewRepository
from infrastructure.spaced_repetition.fsrs_scheduler import FSRSScheduler

class ReviewFlashcardService:

    def __init__(self, session: AsyncSession,
                 user_vocabulary_repository: UserVocabularyRepository, 
                 review_history_repository: ReviewHistoryRepository,
                 review_repository: ReviewRepository,
                 user_repository: UserRepository,
                 fsrs_scheduler: FSRSScheduler):
        self.session=session
        self.user_vocabulary_repository = user_vocabulary_repository
        self.review_history_repository = review_history_repository
        self.review_repository = review_repository
        self.user_repository = user_repository
        self.fsrs_scheduler = fsrs_scheduler

    async def review_flashcard(self, word_id: int, rating: int, user_id: int):
        try:
            user_vocabulary = await self.user_vocabulary_repository.find(user_id, word_id)

            if user_vocabulary is None:
                raise ValueError(
                    "User vocabulary not found"
                )

            now = datetime.now(timezone.utc)

            if user_vocabulary.fsrs_card is None:
                card = self.fsrs_scheduler.create_card()

            else:
                card = self.fsrs_scheduler.deserialize_card(user_vocabulary.fsrs_card)

            new_card, review_log = self.fsrs_scheduler.review(card=card, rating=rating, review_datetime=now)

            user_vocabulary.fsrs_card = self.fsrs_scheduler.serialize_card(new_card)

            user_vocabulary.next_review_at = new_card.due

            await self.user_vocabulary_repository.update(user_vocabulary)

            history = ReviewHistory(
                id=None,
                user_vocabulary_id=user_vocabulary.id,
                rating=rating,
                reviewed_at=review_log.review_datetime,
                scheduled_days = (
                    new_card.due - review_log.review_datetime
                ).total_seconds() / 86400,
            )

            await self.review_history_repository.create(history)

            await self.check_and_increment_streak(user_id)

            await self.session.commit()

            return user_vocabulary
        except Exception:
            await self.session.rollback()
            raise

    async def check_and_increment_streak(self, user_id: int):
        review_statistics = await self.review_repository.get_statistics(user_id=user_id)
        flashcard_statistics = await self.user_vocabulary_repository.get_flashcards_statistics(user_id=user_id)
        
        # Update the user's streak
        user = await self.user_repository.find_by_id(user_id)

        today = date.today()
        
        if (review_statistics.reviews_to_review == 0 
            and review_statistics.overdue_reviews == 0
            and flashcard_statistics.flashcards_to_review + flashcard_statistics.overdue_flashcards == 0
            and user.last_streak_date != today):
            await self.user_repository.update_streak(
                user_id=user_id,
                streak=user.streak + 1,
                last_streak_date=today)