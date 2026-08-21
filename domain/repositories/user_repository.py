
from abc import ABC, abstractmethod

from domain.models.user import User


class UserRepository(ABC):

    @abstractmethod
    async def save(self, user: User) -> User:
        pass

    """ @abstractmethod
    async def update(self, user: User) -> User:
        pass """

    @abstractmethod
    async def find_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    async def find_by_username(self, username: str) -> User | None:
        pass

    @abstractmethod
    async def find_by_id(self, user_id: int) -> User | None:
        pass