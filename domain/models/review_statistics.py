from dataclasses import dataclass


@dataclass
class ReviewStatistics:

    success_rate: float
    reviews_to_review: int
    overdue_reviews: int

