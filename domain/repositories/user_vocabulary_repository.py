
from abc import ABC, abstractmethod

from domain.models.user_vocabulary import UserVocabulary


class UserVocabularyRepository(ABC):

    @abstractmethod
    async def save(self, user_vocabulary: UserVocabulary) -> UserVocabulary:
        pass

    @abstractmethod
    async def update(self, user_vocabulary: UserVocabulary) -> UserVocabulary:
        pass

    @abstractmethod
    async def find(self, user_id: int, vocabulary_word_id: int) -> UserVocabulary | None:
        pass

    @abstractmethod
    async def find_by_id(self, user_vocabulary_id: int) -> UserVocabulary | None:
        pass


