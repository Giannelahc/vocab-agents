
from domain.models.user_preference import UserPreference
from infrastructure.persistence.entities.user_preferences import UserPreferenceModel
from infrastructure.persistence.mappers.language_mapper import LanguageMapper
from infrastructure.persistence.mappers.user_learning_language_mapper import UserLearningLanguageMapper


class UserPreferenceMapper:

    @staticmethod
    def to_entity(model: UserPreferenceModel) -> UserPreference:

        return UserPreference(
            id=model.id,
            user_id=model.user_id,
            native_language_id=model.native_language_id,
            native_language=LanguageMapper.to_entity(model.native_language) if model.native_language is not None else None,
            learning_languages=[
                UserLearningLanguageMapper.to_entity(language)
                for language in model.learning_languages
            ]
        )

    @staticmethod
    def to_model(entity: UserPreference) -> UserPreferenceModel:

        model = UserPreferenceModel(
            id=entity.id,
            user_id=entity.user_id,
            native_language_id=entity.native_language_id
            ##native_language=LanguageMapper.to_model(entity.native_language) if entity.native_language is not None else None
        )

        model.learning_languages = [
            UserLearningLanguageMapper.to_model(language)
            for language in entity.learning_languages
        ]

        return model

