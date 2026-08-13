#domain/models/exercise.py
from dataclasses import dataclass
from typing import Optional

from application.enums.exercise_type import ExerciseType
    
@dataclass
class Exercise:

    type: ExerciseType
    question: str
    options: list[str]
    correct_answer: int

    id: Optional[int] = None

    