
from domain.models.exercise import Exercise
from infrastructure.persistence.entities.exercise import ExerciseModel
from application.enums.exercise_type import ExerciseType as AppExerciseType
from infrastructure.persistence.enums.exercise_type import ExerciseType


class ExerciseMapper:

    @staticmethod
    def to_entity(model: ExerciseModel) -> Exercise:

        return Exercise(
            id=model.id,
            question=model.question,
            options=model.options,
            correct_answer=model.correct_answer,
            type=AppExerciseType(model.type.value)
        )

    @staticmethod
    def to_model(entity: Exercise) -> ExerciseModel:

        model = ExerciseModel(
            id=entity.id,
            question=entity.question,
            options=entity.options,
            correct_answer=entity.correct_answer,
            type=ExerciseType(entity.type.value)
        )

        return model

