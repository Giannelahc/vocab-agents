
from domain.models.example import Example
from entities.example import ExampleModel


class ExampleMapper:

    @staticmethod
    def to_entity(model: ExampleModel) -> Example:

        return Example(
            id=model.id,
            sentence=model.sentence
        )

    @staticmethod
    def to_model(entity: Example) -> ExampleModel:

        model = ExampleModel(
            id=entity.id,
            sentence=entity.sentence
        )

        return model

