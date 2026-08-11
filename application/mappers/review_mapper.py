
from application.enums.review_status import ReviewStatus
from domain.models.exercise import Exercise
from domain.models.review import Review
from domain.models.word_sense import WordSense
from application.enums.exercise_type import ExerciseType

class ReviewMapper:

    def from_analysis(
        self,
        user_vocabulary_id: int,
        exercises: list,
        status: ReviewStatus,
        exercise_type: ExerciseType
    ) -> Review:
        review = Review(user_vocabulary_id=user_vocabulary_id,
                        status=status,
                        exercises=[])

        for exercise_data in exercises:
            exercise = self.to_exercise(exercise_data, exercise_type)
            review.exercises.append(exercise)

        return review


    def to_exercise(self, data: dict, exercise_type: ExerciseType) -> Exercise:

        exercise = Exercise(
            type=exercise_type,
            question=data["question"],
            options=data.get("options"),
            correct_answer=data.get("correct_option"),
        )

        return exercise