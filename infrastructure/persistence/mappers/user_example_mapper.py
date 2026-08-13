
from domain.models.user_example import UserExample
from infrastructure.persistence.entities.user_example import UserExampleModel


class UserExampleMapper:

    @staticmethod
    def to_entity(model: UserExampleModel) -> UserExample:

        return UserExample(
            id=model.id,
            word_sense_id=model.word_sense_id,
            sentence=model.sentence
        )

    @staticmethod
    def to_model(entity: UserExample) -> UserExampleModel:

        return UserExampleModel(
            id=entity.id,
            word_sense_id=entity.word_sense_id,
            sentence=entity.sentence
        )

