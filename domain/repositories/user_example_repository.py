
from abc import ABC, abstractmethod

from domain.models.user_example import UserExample


class UserExampleRepository(ABC):

    @abstractmethod
    async def find_user_vocabulary_id(self, user_id: int, word_sense_id: int) -> int | None:
        pass

    @abstractmethod
    async def save_all(self, user_example: list[UserExample]) -> list[UserExample]:
        pass

    
