from domain.models.language import Language
from domain.repositories.language_repository import LanguageRepository

class LanguageService:
    def __init__(self,  language_repository: LanguageRepository):
        self.language_repository = language_repository

    async def get_languages(self) -> list[Language]:
        return await self.language_repository.find_all()

