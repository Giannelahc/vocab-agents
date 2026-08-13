

from fastapi import APIRouter, BackgroundTasks, Depends, Query, status

from dependencies import get_current_user, get_review_service
from api.mappers.review_mapper import ReviewMapper
from schemas.review import ExerciseRequest
from application.services.review_service import ReviewService
from application.enums.review_status import ReviewStatus

router = APIRouter()

@router.post("/{review_id}/complete")
async def complete_review(
    review_id: int,
    request: list[ExerciseRequest],
    background_tasks: BackgroundTasks,
    user_id: int = Depends(get_current_user),
    service: ReviewService = Depends(get_review_service)
):
    exercise_list = ReviewMapper.to_entity_list(request)
    review, next_review = await service.complete_review(review_id, user_id, exercise_list)
    background_tasks.add_task(
        service.generate_review,
        user_id=user_id,
        review=next_review
    )
    return ReviewMapper.to_response(review)

@router.post("/regenerate", status_code=status.HTTP_202_ACCEPTED)
async def generate_failed_reviews(
    background_tasks: BackgroundTasks,
    user_id: int = Depends(get_current_user),
    service: ReviewService = Depends(get_review_service)):

    failed_reviews = await service.get_failed_reviews(user_id)

    for review in failed_reviews:
        background_tasks.add_task(
            service.generate_review,
            user_id,
            review
        )

    return {
        "message": "Review generation started",
        "reviews_count": len(failed_reviews)
    }


@router.get("/next")
async def get_pending_reviews(
    user_id: int = Depends(get_current_user),
    service: ReviewService = Depends(get_review_service)
):
    reviews = await service.get_pending_reviews(user_id)
    return ReviewMapper.to_list_response(reviews)

@router.get("")
async def get_reviews(
    status: ReviewStatus | None = Query(None),
    user_id: int = Depends(get_current_user),
    service: ReviewService = Depends(get_review_service)
):
    reviews = await service.get_reviews(user_id, status)
    return ReviewMapper.to_list_response(reviews)
    
