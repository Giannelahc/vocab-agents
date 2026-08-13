
from abc import ABC, abstractmethod

from domain.models.user_example import UserExample


class UserExampleRepository(ABC):

    @abstractmethod
    async def save_all(self, user_example: list[UserExample]) -> list[UserExample]:
        pass

    
