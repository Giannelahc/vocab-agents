import random
import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from agents.exercise_agent import ExerciseAgent
from domain.models.word_sense import WordSense
from domain.repositories.review_repository import ReviewRepository
from domain.repositories.user_vocabulary_repository import UserVocabularyRepository
from domain.repositories.language_repository import LanguageRepository
from application.enums.exercise_type import ExerciseType
from domain.models.vocabulary_word import VocabularyWord
from application.services.user_preference import UserPreferenceService
from application.mappers.review_mapper import ReviewMapper
from application.enums.review_status import ReviewStatus
from domain.models.review import Review

class ReviewService:
    def __init__(self,  session: AsyncSession, 
                 review_repository: ReviewRepository, 
                 user_vocabulary_repository: UserVocabularyRepository,
                 language_repository: LanguageRepository,
                 user_preference_service: UserPreferenceService,
                 exercise_agent: ExerciseAgent,
                 review_mapper: ReviewMapper):
        self.session=session
        self.review_repository = review_repository
        self.user_vocabulary_repository = user_vocabulary_repository
        self.language_repository = language_repository
        self.user_preference_service = user_preference_service
        self.exercise_agent = exercise_agent
        self.review_mapper = review_mapper

    async def generate_review(self, user_id: int, vocabulary_word: VocabularyWord):
        try:
            user_vocabulary = await self.user_vocabulary_repository.find(user_id, vocabulary_word.id)
            preferences = await self.user_preference_service.get_user_preferences(user_id)
            native_language = preferences.native_language if preferences else None
            language = await self.language_repository.find_by_id(vocabulary_word.language_id)

            exercise_type = ExerciseType(user_vocabulary.review_level) if user_vocabulary else ExerciseType.MULTIPLE_CHOICE_DEFINITION

            exercises = []
            for tag in vocabulary_word.senses:
                correct_answer = self.determine_correct_answer(exercise_type, tag, native_language.code)
                exercises.append(self.exercise_agent.generate_exercises(
                                exercise_type=exercise_type,
                                word=vocabulary_word.word,
                                correct_answer=correct_answer,
                                tag=tag,
                                target_language=language.code,
                                native_language=native_language.code
                            ))
            result = await asyncio.gather(*exercises)

            review = await self.build_new_review(user_vocabulary.id, result, exercise_type)

            await self.review_repository.save(review)

            await self.session.commit()

            return review

        except Exception:
            await self.session.rollback()
            raise

    

    async def build_new_review(self, user_vocabulary_id: int, exercises: list, 
                               exercise_type: ExerciseType) -> Review:
        return self.review_mapper.from_analysis(user_vocabulary_id, exercises, ReviewStatus.PENDING, exercise_type)


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
            

    def get_random_translation(word_sense: WordSense, native_language_code: str) -> str:
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

