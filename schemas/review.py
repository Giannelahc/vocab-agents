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