# infrastructure/persistence/language_initializer.py

from infrastructure.persistence.entities.language import LanguageModel
from infrastructure.repositories.sql_language_repository import SQLLanguageRepository


class LanguageInitializer:

    def __init__(self, repository: SQLLanguageRepository):
        self.repository = repository

    async def initialize(self):

        language_count = await self.repository.count()
        if language_count > 0:
            return

        default_languages = [
            LanguageModel(code="fr", name="French"),
            LanguageModel(code="en", name="English"),
            LanguageModel(code="es", name="Spanish"),
            LanguageModel(code="it", name="Italian"),
            LanguageModel(code="de", name="German"),
            LanguageModel(code="pt", name="Portuguese"),
        ]

        await self.repository.save_all(default_languages)