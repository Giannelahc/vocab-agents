import random
import asyncio
import traceback

from sqlalchemy.ext.asyncio import AsyncSession
from agents.exercise_agent import ExerciseAgent
from domain.models.word_sense import WordSense
from domain.repositories.review_repository import ReviewRepository
from domain.repositories.user_vocabulary_repository import UserVocabularyRepository
from domain.repositories.vocabulary_word_repository import VocabularyWordRepository
from domain.repositories.language_repository import LanguageRepository
from application.enums.exercise_type import ExerciseType
from domain.models.review_statistics import ReviewStatistics
from domain.models.review_home import ReviewHome
from application.services.user_preference import UserPreferenceService
from application.services.review_scheduler import ReviewScheduler
from application.mappers.review_mapper import ReviewMapper
from application.enums.review_status import ReviewStatus
from application.enums.generation_status import GenerationStatus
from domain.models.review import Review
from domain.models.review_summary import ReviewSummary
from domain.models.exercise_answer import ExerciseAnswer

class ReviewService:
    def __init__(self,  session: AsyncSession, 
                 review_repository: ReviewRepository, 
                 user_vocabulary_repository: UserVocabularyRepository,
                 vocabulary_word_repository: VocabularyWordRepository,
                 language_repository: LanguageRepository,
                 user_preference_service: UserPreferenceService,
                 exercise_agent: ExerciseAgent,
                 review_mapper: ReviewMapper):
        self.session=session
        self.review_repository = review_repository
        self.user_vocabulary_repository = user_vocabulary_repository
        self.vocabulary_word_repository = vocabulary_word_repository
        self.language_repository = language_repository
        self.user_preference_service = user_preference_service
        self.exercise_agent = exercise_agent
        self.review_mapper = review_mapper

    async def register_review(self, user_vocabulary_id: int) -> Review:
        review = Review(
            user_vocabulary_id=user_vocabulary_id, 
            status=ReviewStatus.PENDING,
            generation_status=GenerationStatus.TO_GENERATE,
            exercises=[])
        return await self.review_repository.save(review)

    async def generate_review(self, user_id: int, review: Review):
        try:
            await self.update_generation_status(review.id, GenerationStatus.GENERATING)

            user_vocabulary = await self.user_vocabulary_repository.find_by_id(review.user_vocabulary_id)
            preferences = await self.user_preference_service.get_user_preferences(user_id)
            native_language = preferences.native_language if preferences else None

            vocabulary_word = await self.vocabulary_word_repository.find_by_id(user_vocabulary.vocabulary_word_id)

            language = await self.language_repository.find_by_id(vocabulary_word.language_id)

            exercise_type = ExerciseType(user_vocabulary.review_level) if user_vocabulary else ExerciseType.MULTIPLE_CHOICE_DEFINITION

            exercises = []
            for word_sense in vocabulary_word.senses:
                correct_answer = self.determine_correct_answer(exercise_type, word_sense, native_language.code)
                exercises.append(self.exercise_agent.generate_exercises(
                                exercise_type=exercise_type,
                                word=vocabulary_word.word,
                                correct_answer=correct_answer,
                                tag=word_sense.grammar_type,
                                target_language=language.code,
                                native_language=native_language.code
                            ))
            result = await asyncio.gather(*exercises)

            ##update generating status to READY
            await self.update_review_with_exercises(result, exercise_type, review)

            await self.session.commit()

            return review

        except Exception:
            await self.session.rollback()
            await self.update_generation_status(review.id, GenerationStatus.FAILED)
            await self.session.commit()
            traceback.print_exc()

    async def complete_review(self, review_id: int, user_id: int, answers: list[ExerciseAnswer]):
        try:
            review = await self.review_repository.find_by_id(review_id)

            if review is None:
                raise ValueError("Review not found")

            user_vocabulary = await self.user_vocabulary_repository.find_by_id(review.user_vocabulary_id)

            if user_vocabulary is None:
                raise ValueError("User vocabulary not found")

            answers_by_exercise = {
                answer.id: answer.answer
                for answer in answers
            }

            passed = True

            for exercise in review.exercises:
                user_answer = answers_by_exercise.get(exercise.id)

                if user_answer is None:
                    passed = False
                    break

                if user_answer != exercise.correct_answer:
                    passed = False
                    break

            review.status = (
                ReviewStatus.PASSED
                if passed
                else ReviewStatus.FAILED
            )

            if passed:
                user_vocabulary.review_level+=1
                user_vocabulary.next_review_at=(
                    ReviewScheduler.schedule_next_review(
                    user_vocabulary.review_level
                    )
                )
            else:
                user_vocabulary.next_review_at=ReviewScheduler.schedule_next_review(0)

            ##update FAILED or PASSED
            await self.review_repository.update_status(review_id=review.id, status=review.status)

            ##update next_level and next_review_at
            await self.user_vocabulary_repository.update(user_vocabulary)

            ##Create next new review
            next_review = await self.register_review(user_vocabulary.id)

            await self.session.commit()

            return review, next_review, user_vocabulary.next_review_at

        except Exception:
            await self.session.rollback()
            raise

    async def get_reviews(self, user_id: int, page: int = 1, page_size: int = 50, status: ReviewStatus | None = None) -> tuple[list[ReviewSummary], int]:
        return await self.review_repository.get_reviews(user_id, status, False, page, page_size)

    async def get_review_detail_by_id(self, review_id: int) -> Review:
        return await self.review_repository.find_by_id(review_id)

    async def get_pending_reviews(self, user_id: int, page: int = 1, page_size: int = 50) -> tuple[list[ReviewSummary], int]:
        return await self.review_repository.get_reviews(user_id, ReviewStatus.PENDING, True, page, page_size)

    async def get_failed_reviews(self, user_id: int) -> list[Review]:
        return await self.review_repository.get_failed_reviews(user_id)

    async def update_generation_status(self, review_id: int, status: GenerationStatus):
        await self.review_repository.update_generation_status(review_id, status)

    async def update_review_with_exercises(self, exercises: list, 
                               exercise_type: ExerciseType, review: Review):
        self.review_mapper.from_analysis(exercises, GenerationStatus.READY, exercise_type, review)
        await self.review_repository.update_exercises(review)

    async def get_pending_review_by_user_vocabulary_id(self, user_vocabulary_id: int) -> Review:
        return await self.review_repository.find_by_user_vocabulary_id_and_status(user_vocabulary_id, ReviewStatus.PENDING)

    async def get_home(self, user_id: int) -> ReviewHome:

        statistics = await self.review_repository.get_statistics(
            user_id
        )

        pending_reviews, _ = await self.get_pending_reviews(
            user_id=user_id,
            page_size=5
        )

        return ReviewHome(
            statistics=statistics,
            pending_reviews= pending_reviews
        )

    def determine_correct_answer(self, exercise_type: ExerciseType, 
                                       word_sense: WordSense, 
                                       native_language_code: str) -> str:
        match exercise_type:
            case ExerciseType.MULTIPLE_CHOICE_DEFINITION:
                return word_sense.definition
            case ExerciseType.MULTIPLE_CHOICE_TRANSLATION:
                return self.get_random_translation(word_sense, native_language_code)
            case ExerciseType.FILL_IN_THE_BLANK:
                synonym = random.choice(word_sense.synonyms).word if word_sense.synonyms else ""
                return synonym
            case _:
                return word_sense.definition
            

    def get_random_translation(self, word_sense: WordSense, native_language_code: str) -> str:
        translations = None
        # safe attribute access in case model differs
        if hasattr(word_sense, "translations") and isinstance(word_sense.translations, dict):
            translations = word_sense.translations.get(native_language_code)

        # If translations is missing or empty, fall back to empty string
        if not translations:
            return ""

        # Choose a random translation from the list
        try:
            return random.choice(translations)
        except (IndexError, TypeError):
            return ""

