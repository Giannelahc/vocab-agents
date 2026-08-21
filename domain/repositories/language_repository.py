
from abc import ABC, abstractmethod

from domain.models.language import Language


class LanguageRepository(ABC):

    @abstractmethod
    async def save(self, language: Language) -> Language:
        pass

    @abstractmethod
    async def find_by_id(self, language_id: int) -> Language | None:
        pass

    @abstractmethod
    async def count(self) -> int:
        pass

    @abstractmethod
    async def save_all(self, languages: list[Language]) -> list[Language]:
        pass

    @abstractmethod
    async def find_all(self) -> list[Language]:
        pass 

    
