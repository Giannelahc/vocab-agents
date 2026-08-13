
from domain.models.review import Review
from domain.models.exercise import Exercise
from domain.models.exercise_answer import ExerciseAnswer
from schemas.review import ReviewResponse, ExerciseResponse, ExerciseRequest
from application.enums.review_status import ReviewStatus


class ReviewMapper:

    @staticmethod
    def to_entity_list(request_list: list[ExerciseRequest]) -> list[ExerciseAnswer]:
        exercise_answer_list = [
                ReviewMapper.to_entity(exercise)
                for exercise in request_list
                ]
        return exercise_answer_list

    @staticmethod
    def to_entity(request: ExerciseRequest) -> ExerciseAnswer:
        return ExerciseAnswer(
            id= request.id,
            answer=request.answer
        )

    @staticmethod
    def to_list_response(entity_list: list[Review]) -> list[ReviewResponse]:
        review_list = [
                ReviewMapper.to_response(review)
                for review in entity_list
                ]
        return review_list

    @staticmethod
    def to_response(entity: Review) -> ReviewResponse:
        review_response = ReviewResponse(
            id=entity.id,
            user_vocabulary_id=entity.user_vocabulary_id,
            status=entity.status.value,
            exercises=[
                ExerciseMapper.to_response(exercise) 
                for exercise in entity.exercises
                ]
        )
        return review_response


class ExerciseMapper:

    @staticmethod
    def to_response(entity: Exercise) -> ExerciseResponse:
        exercise_response = ExerciseResponse(
            id=entity.id,
            type=entity.type.name,
            question=entity.question,
            options=entity.options,
            correct_answer=entity.correct_answer
        )
        return exercise_response