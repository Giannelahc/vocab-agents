from domain.models.vocabulary_word import VocabularyWord
from domain.repositories.vocabulary_word_repository import VocabularyWordRepository

class VocabularyWordService:
    def __init__(self,  vocabulary_word_repository: VocabularyWordRepository):
        self.vocabulary_word_repository = vocabulary_word_repository

    async def get_words_by_user(self, user_id: int, language_id: int, page: int, page_size: int) -> list[VocabularyWord]:
        return await self.vocabulary_word_repository.find_by_user_id(user_id, language_id, page, page_size)

