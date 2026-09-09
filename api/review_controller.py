

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
    review, next_review, next_review_at = await service.complete_review(review_id, user_id, exercise_list)
    background_tasks.add_task(
        service.generate_review,
        user_id=user_id,
        review=next_review
    )
    return {
        "id": review.id,
        "status": review.status,
        "next_review_at": next_review_at
    }

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
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    service: ReviewService = Depends(get_review_service)
):
    reviews, total = await service.get_pending_reviews(user_id, page, page_size)
    return ReviewMapper.to_summary_list_response_paginated(reviews, page, page_size, total)

@router.get("")
async def get_reviews(
    status: ReviewStatus | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    user_id: int = Depends(get_current_user),
    service: ReviewService = Depends(get_review_service)
):
    reviews, total = await service.get_reviews(user_id, page, page_size, status)
    return ReviewMapper.to_summary_list_response_paginated(reviews, page, page_size, total)

@router.get("/home")
async def get_review_home(
    user_id: int = Depends(get_current_user),
    service: ReviewService = Depends(get_review_service)
):
    review_statistics = await service.get_home(user_id)
    return ReviewMapper.to_review_home_response(review_statistics)
    
@router.get("/{review_id}")
async def get_review_by_id(
    review_id: int,
    user_id: int = Depends(get_current_user),
    service: ReviewService = Depends(get_review_service)
):
    review = await service.get_review_detail_by_id(review_id)
    return ReviewMapper.to_response(review)