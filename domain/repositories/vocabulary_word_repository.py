
from abc import ABC, abstractmethod

from domain.models.vocabulary_word import VocabularyWord
from application.enums.vocabulary_status import VocabularyStatus


class VocabularyWordRepository(ABC):

    @abstractmethod
    async def save(self, vocabulary_word: VocabularyWord) -> VocabularyWord:
        pass

    @abstractmethod
    async def update_status(self, vocabulary_word_id: int, status: VocabularyStatus) -> None:
        pass    

    @abstractmethod
    async def update_senses(self, vocabulary_word: VocabularyWord) -> VocabularyWord:
        pass

    @abstractmethod
    async def find_by_word_and_language(self, word: str, language_id: int) -> VocabularyWord | None: 
        pass

    @abstractmethod
    async def find_by_id(self, vocabulary_word_id: int) -> VocabularyWord | None:
        pass
