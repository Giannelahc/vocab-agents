
from domain.models.language import Language
from infrastructure.persistence.entities.language import LanguageModel


class LanguageMapper:

    @staticmethod
    def to_entity(model: LanguageModel) -> Language:

        return Language(
            id=model.id,
            code=model.code,
            name=model.name
        )

    @staticmethod
    def to_model(entity: Language) -> LanguageModel:

        return LanguageModel(
            code=entity.code,
            name=entity.name
        )

