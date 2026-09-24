
from domain.models.review import Review
from domain.models.review_history import ReviewHistory
from domain.models.review_summary import ReviewSummary
from infrastructure.persistence.entities.review import ReviewModel
from infrastructure.persistence.entities.review_history import ReviewHistoryModel
from infrastructure.persistence.enums.review_status import ReviewStatus
from infrastructure.persistence.enums.generation_status import GenerationStatus
from infrastructure.persistence.mappers.exercise_mapper import ExerciseMapper


class ReviewHistoryMapper:

    @staticmethod
    def to_entity(model: ReviewHistoryModel) -> ReviewHistory:
        return ReviewHistory(
            id=model.id,
            user_vocabulary_id=model.user_vocabulary_id,
            rating=model.rating,
            reviewed_at=model.reviewed_at,
            scheduled_days=model.scheduled_days
        )


    @staticmethod
    def to_model(entity: ReviewHistory) -> ReviewHistoryModel:
        return ReviewHistoryModel(
            id=entity.id,
            user_vocabulary_id=entity.user_vocabulary_id,
            rating=entity.rating,
            reviewed_at=entity.reviewed_at,
            scheduled_days=entity.scheduled_days
        )