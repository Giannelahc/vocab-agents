from domain.repositories.language_repository import LanguageRepository
from domain.repositories.user_vocabulary_repository import UserVocabularyRepository
from domain.repositories.vocabulary_word_repository import VocabularyWordRepository
from agents.vocabulary_identification_agent import VocabularyIdentificationAgent
from domain.models.vocabulary_candidate import VocabularyCandidate
from application.mappers.vocabulary_candidate_mapper import VocabularyCandidateMapper

class VocabularyIdentifierService:

    def __init__(
        self,
        identification_agent: VocabularyIdentificationAgent,
        language_repository: LanguageRepository,
        vocabulary_word_repository: VocabularyWordRepository
    ):
        self.identification_agent = identification_agent
        self.language_repository = language_repository
        self.vocabulary_word_repository = vocabulary_word_repository

    async def identify(
        self,
        text: str,
        language_id: int,
        user_id: int
    ):
        language = await self.language_repository.find_by_id(language_id)

        if language is None:
            raise ValueError("Language not found")

        response = await self.identification_agent.process_text(
            text=text,
            target_language=language.code
        )

        candidates = VocabularyCandidateMapper.to_candidates(response)

        candidates = self.remove_duplicates(candidates)

        candidates = await self.mark_existing_words(
            candidates,
            user_id,
            language_id
        )

        return candidates

    def remove_duplicates(
        self,
        candidates: list[VocabularyCandidate]
    ) -> list[VocabularyCandidate]:

        unique = []
        seen = set()

        for candidate in candidates:
            key = (
                candidate.text.strip().lower(),
                candidate.type
            )

            if key in seen:
                continue

            seen.add(key)
            unique.append(candidate)

        return unique

    async def mark_existing_words(
        self,
        candidates: list[VocabularyCandidate],
        user_id: int,
        language_id: int
    ) -> list[VocabularyCandidate]:

        words = list({
            candidate.text.strip().lower()
            for candidate in candidates
        })

        existing_words = await (
            self.vocabulary_word_repository.find_existing_words(
                user_id=user_id,
                language_id=language_id,
                words=words
            )
        )

        for candidate in candidates:
            normalized_text = candidate.text.strip().lower()

            candidate.already_registered = (
                normalized_text in existing_words
            )

        return candidates