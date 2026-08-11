#domain/models/exercise.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from application.enums.exercise_type import ExerciseType
    
@dataclass
class Exercise:

    type: ExerciseType
    question: str
    options: list[str]
    correct_answer: str

    id: Optional[int] = None

    