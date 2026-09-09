from dataclasses import dataclass

from domain.models.review_statistics import ReviewStatistics
from domain.models.review_summary import ReviewSummary


@dataclass
class ReviewHome:

    statistics: ReviewStatistics
    pending_reviews: list[ReviewSummary]

