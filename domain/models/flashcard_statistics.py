from dataclasses import dataclass
from datetime import datetime


@dataclass
class FlashcardStatistics:
    flashcards_to_review: int
    overdue_flashcards: int
    flashcards_active: bool