from datetime import datetime, timezone

from fsrs import (
    Card,
    Rating,
    Scheduler,
)


class FSRSScheduler:

    def __init__(self):
        self.scheduler = Scheduler(
            desired_retention=0.9,
            enable_fuzzing=False,
        )

    def create_card(self) -> Card:
        return Card()

    def review(self, card: Card, rating: int, review_datetime: datetime) -> tuple[Card, object]:

        fsrs_rating = Rating(rating)

        return self.scheduler.review_card(card=card, rating=fsrs_rating, review_datetime=review_datetime)

    def serialize_card(self, card: Card) -> dict:
        return card.to_dict()

    def deserialize_card(self, data: dict) -> Card:
        return Card.from_dict(data)