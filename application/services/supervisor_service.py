
# application/services/supervisor_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from agents.supervisor_agent import SupervisorAgent
from application.enums.vocabulary_status import VocabularyStatus
from application.mappers.vocabulary_mapper import VocabularyMapper
from application.services.review_scheduler import ReviewScheduler
from domain.models.vocabulary_word import VocabularyWord
from domain.repositories.vocabulary_word_repository import VocabularyWordRepository
from domain.repositories.user_vocabulary_repository import UserVocabularyRepository
from domain.repositories.language_repository import LanguageRepository
from application.services.user_preference import UserPreferenceService
from domain.models.user_vocabulary import UserVocabulary


class SupervisorService:

    def __init__(self, session: AsyncSession, 
                 vocabulary_repository: VocabularyWordRepository, 
                 user_vocabulary_repository: UserVocabularyRepository,
                 language_repository: LanguageRepository,
                 user_preference_service: UserPreferenceService,
                 supervisor_agent: SupervisorAgent,
                 vocabulary_mapper: VocabularyMapper):
        self.session = session
        self.vocabulary_repository = vocabulary_repository
        self.language_repository = language_repository
        self.user_preference_service = user_preference_service
        self.supervisor_agent = supervisor_agent
        self.vocabulary_mapper = vocabulary_mapper
        self.user_vocabulary_repository = user_vocabulary_repository

    async def register_word(self, word: str, language_id: int, user_id: int):
        existing = await self.vocabulary_repository.find_by_word_and_language(word, language_id)

        if existing:
            relation = await self.user_vocabulary_repository.find(user_id, existing.id)

            if relation is None:
                await self.user_vocabulary_repository.save(
                    UserVocabulary(
                        user_id=user_id,
                        vocabulary_word_id=existing.id
                    )
                )

            return existing

        vocabulary = VocabularyWord(
            id=None,
            word=word,
            language_id=language_id,
            status=VocabularyStatus.PENDING
        )

        saved_word = await self.vocabulary_repository.save(vocabulary)


        await self.user_vocabulary_repository.save(
            UserVocabulary(
                user_id=user_id,
                vocabulary_word_id=saved_word.id,
                review_level=0,
                next_review_at=ReviewScheduler.schedule_first_review(0)
            )
        )

        return saved_word

    async def process_word(self, user_id: int, vocabulary_id: int):
        vocabulary = await self.vocabulary_repository.find_by_id(vocabulary_id)

        try:

            await self.vocabulary_repository.update_status(vocabulary_id, VocabularyStatus.PROCESSING)

            await self.session.commit()

            analysis = await self.build_analysis(vocabulary.word, vocabulary.language_id, user_id)

            await self.save_analysis(vocabulary, analysis)
            await self.session.commit()

        except Exception:
            await self.session.rollback()
            await self.vocabulary_repository.update_status(vocabulary_id, VocabularyStatus.FAILED)
            await self.session.commit()
            raise


    async def get_target_languages(self, user_id, language_code):
        pref = await self.user_preference_service.get_user_preferences(user_id)

        target_languages = [
            lang.language.code for lang in pref.learning_languages
        ]
        
        if pref.native_language.code not in target_languages:
            target_languages.append(pref.native_language.code)
        if language_code in target_languages:
            target_languages.remove(language_code)
        return target_languages

    async def build_analysis(self, word: str, language_id: int, user_id: int):
        language = await self.language_repository.find_by_id(language_id)
        target_languages = await self.get_target_languages(user_id, language.code)
        analysis = await self.supervisor_agent.run(word, target_languages, language.code)
        return analysis

    async def save_analysis(self, vocabulary: VocabularyWord, analysis: dict):
        
        vocabulary.senses = self.vocabulary_mapper.from_analysis(analysis)
        vocabulary.status = VocabularyStatus.COMPLETED
        saved_word = await self.vocabulary_repository.update_senses(vocabulary)

        return saved_word
