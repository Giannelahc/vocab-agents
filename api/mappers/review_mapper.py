
from domain.models.review import Review
from domain.models.review_summary import ReviewSummary
from domain.models.exercise import Exercise 
from domain.models.review_home import ReviewHome 
from domain.models.review_statistics import ReviewStatistics 
from domain.models.exercise_answer import ExerciseAnswer
from schemas.review import (ReviewResponse, ReviewSummaryResponse, 
                            ReviewSummaryPaginatedResponse, ExerciseResponse, 
                            ExerciseRequest, ReviewHomeResponse, ReviewStatisticsResponse)
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
    def to_summary_list_response(
        entity_list: list[ReviewSummary]
    ) -> list[ReviewSummaryResponse]:
        return [
            ReviewMapper.to_summary_response(review)
            for review in entity_list
        ]

    @staticmethod
    def to_summary_list_response_paginated(
        entity_list: list[ReviewSummary],
        page: int,
        page_size: int,
        total: int
    ) -> ReviewSummaryPaginatedResponse:
        return ReviewSummaryPaginatedResponse(
            page= page,
            page_size= page_size,
            total= total,
            items= [
                    ReviewMapper.to_summary_response(review)
                    for review in entity_list
                ]
        )

    @staticmethod
    def to_review_statistics(entity: ReviewStatistics) -> ReviewStatisticsResponse:
        return ReviewStatisticsResponse(
            overdue_reviews=entity.overdue_reviews,
            reviews_to_review=entity.reviews_to_review,
            success_rate=entity.success_rate
        )

    @staticmethod
    def to_review_home_response(entity: ReviewHome) -> ReviewHomeResponse:
        return ReviewHomeResponse(
            statistics=ReviewMapper.to_review_statistics(entity.statistics),
            pending_reviews=[
                    ReviewMapper.to_summary_response(review)
                    for review in entity.pending_reviews
                ]
        )

    @staticmethod
    def to_summary_response(entity: ReviewSummary) -> ReviewSummaryResponse:
        return ReviewSummaryResponse(
            id=entity.id,
            status=entity.status.value,
            user_vocabulary_id=entity.user_vocabulary_id,
            word=entity.word,
            review_level=entity.review_level,
            next_review_at=entity.next_review_at,
            completed_at=entity.completed_at,
            exercises=entity.exercises
        )

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