# schemas/review.py
from pydantic import BaseModel
from datetime import datetime

class ExerciseRequest(BaseModel):
    id: int | None = None
    answer: int

class ExerciseResponse(BaseModel):
    id: int | None = None
    type: str
    question: str
    options: list[str]
    correct_answer: int


class ReviewResponse(BaseModel):
    id: int | None = None
    status: str
    user_vocabulary_id: int
    completed_at: datetime | None = None
    exercises: list[ExerciseResponse]

class ReviewSummaryResponse(BaseModel):
    id: int | None = None
    status: str
    user_vocabulary_id: int
    word: str
    review_level: int
    next_review_at: datetime
    completed_at: datetime | None = None
    exercises: int = 0

class ReviewSummaryPaginatedResponse(BaseModel):
    page: int
    page_size: int
    total: int
    items: list[ReviewSummaryResponse]

class ReviewStatisticsResponse(BaseModel):
    success_rate: float
    reviews_to_review: int
    overdue_reviews: int

class ReviewHomeResponse(BaseModel):
    statistics: ReviewStatisticsResponse
    pending_reviews: list[ReviewSummaryResponse]