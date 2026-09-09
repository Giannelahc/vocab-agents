
from domain.models.user_learning_language import UserLearningLanguage
from domain.models.user_preference import UserPreference
from domain.models.language import Language
from schemas.preference import UserPreferenceDto, LanguageDto, UserPreferenceRequest


class UserPreferenceMapper:

    @staticmethod
    def to_entity(request: UserPreferenceRequest, user_id: int) -> UserPreference:

        return UserPreference(
            id=request.id,
            native_language_id=request.native_language_id,
            user_id=user_id,
            learning_languages=[
                UserLearningLanguageMapper.to_entity(language)
                for language in request.learning_languages_ids
                ]
        )

    @staticmethod
    def to_response(entity: UserPreference) -> UserPreferenceRequest:

        response = UserPreferenceRequest(
            id=entity.id,
            native_language_id=entity.native_language_id,
            learning_languages_ids=[
                language.language_id
                for language in entity.learning_languages
                ] 
        )

        return response

    @staticmethod
    def to_dto(entity: UserPreference) -> UserPreferenceDto:

        model = UserPreferenceDto(
            id=entity.id,
            native_language=LanguageMapper.to_request(entity.native_language) if entity.native_language is not None else None,
            learning_languages=[
                LanguageMapper.to_request(language.language)
                for language in entity.learning_languages
                if language.language is not None
            ] if entity.learning_languages is not None else []
        )

        return model


class UserLearningLanguageMapper:

    @staticmethod
    def to_entity(language_id: int) -> UserLearningLanguage:

        return UserLearningLanguage(
            language_id=language_id
        )

class LanguageMapper:

    @staticmethod
    def to_request(entity: Language | None) -> LanguageDto | None:
        if entity is None:
            return None

        return LanguageDto(id=entity.id, code=entity.code, name=entity.name)
    