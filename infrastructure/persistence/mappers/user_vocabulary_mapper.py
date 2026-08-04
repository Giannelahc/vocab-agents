
from domain.models.user_vocabulary import UserVocabulary
from entities.user_vocabulary import UserVocabularyModel


class UserVocabularyMapper:

    @staticmethod
    def to_entity(model: UserVocabularyModel) -> UserVocabulary:

        return UserVocabulary(
            id=model.id,
            user_id=model.user_id,
            vocabulary_word_id=model.vocabulary_word_id,
            learned=model.learned,
            favorite=model.favorite,
            review_level=model.review_level,
            next_review_at=model.next_review_at,
            last_review_at=model.last_review_at,
            created_at=model.created_at
        )

    @staticmethod
    def to_model(entity: UserVocabulary) -> UserVocabularyModel:

        return UserVocabularyModel(
            id=entity.id,
            user_id=entity.user_id,
            vocabulary_word_id=entity.vocabulary_word_id,
            learned=entity.learned,
            favorite=entity.favorite,
            review_level=entity.review_level,
            next_review_at=entity.next_review_at,
            last_review_at=entity.last_review_at,
            created_at=entity.created_at
        )