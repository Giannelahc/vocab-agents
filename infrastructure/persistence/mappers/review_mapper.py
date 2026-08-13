
from domain.models.review import Review
from infrastructure.persistence.entities.review import ReviewModel
from infrastructure.persistence.enums.review_status import ReviewStatus
from infrastructure.persistence.enums.generation_status import GenerationStatus
from application.enums.review_status import ReviewStatus as AppReviewStatus
from application.enums.generation_status import GenerationStatus as AppGenerationStatus
from infrastructure.persistence.mappers.exercise_mapper import ExerciseMapper


class ReviewMapper:

    @staticmethod
    def to_entity(model: ReviewModel) -> Review:

        return Review(
            id=model.id,
            user_vocabulary_id=model.user_vocabulary_id,
            completed_at=model.completed_at,
            status=AppReviewStatus(model.status.value),
            generation_status=AppGenerationStatus(model.generation_status.value),
            exercises=[
                ExerciseMapper.to_entity(exercise)
                for exercise in model.exercises
            ]
        )

    @staticmethod
    def to_model(entity: Review) -> ReviewModel:

        model = ReviewModel(
            id=entity.id,
            user_vocabulary_id=entity.user_vocabulary_id,
            completed_at=entity.completed_at,
            status=ReviewStatus(entity.status.value),
            generation_status=GenerationStatus(entity.generation_status.value)
        )

        model.exercises = [
            ExerciseMapper.to_model(exercise)
            for exercise in entity.exercises
        ]

        return model
