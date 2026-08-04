
from abc import ABC, abstractmethod

from domain.models.user_preference import UserPreference


class UserPreferenceRepository(ABC):

    @abstractmethod
    async def save(self, user_preference: UserPreference) -> UserPreference:
        pass

    @abstractmethod
    async def find_by_user_id(self, user_id: int) -> UserPreference | None:
        pass
