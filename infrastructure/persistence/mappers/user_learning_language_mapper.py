
from domain.models.user_learning_language import UserLearningLanguage
from infrastructure.persistence.entities.user_learning_language import UserLearningLanguageModel
from infrastructure.persistence.mappers.language_mapper import LanguageMapper


class UserLearningLanguageMapper:

    @staticmethod
    def to_entity(model: UserLearningLanguageModel) -> UserLearningLanguage:

        return UserLearningLanguage(
            id=model.id,
            language_id=model.language_id,
            language=LanguageMapper.to_entity(model.language) if model.language is not None else None
        )

    @staticmethod
    def to_model(entity: UserLearningLanguage) -> UserLearningLanguageModel:

        return UserLearningLanguageModel(
            id=entity.id,
            language_id=entity.language_id
            ##language=LanguageMapper.to_model(entity.language) if entity.language is not None else None
        )

