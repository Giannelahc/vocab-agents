#domain/models/exercise.py
from dataclasses import dataclass

@dataclass
class ExerciseAnswer:

    id: int 
    answer: int

    