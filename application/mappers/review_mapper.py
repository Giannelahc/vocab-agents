
from application.enums.generation_status import GenerationStatus
from domain.models.exercise import Exercise
from domain.models.review import Review
from domain.models.word_sense import WordSense
from application.enums.exercise_type import ExerciseType

class ReviewMapper:

    def from_analysis(
        self,
        exercises: list,
        status: GenerationStatus,
        exercise_type: ExerciseType,
        review: Review
    ):
        review.exercises = []
        for exercise_data in exercises:
            exercise = self.to_exercise(exercise_data, exercise_type)
            review.exercises.append(exercise)
        review.generation_status= status


    def to_exercise(self, data: dict, exercise_type: ExerciseType) -> Exercise:

        exercise = Exercise(
            type=exercise_type,
            question=data["question"],
            options=data.get("options"),
            correct_answer=(int(data.get("correct_option")) if data.get("correct_option") is not None else None),
        )

        return exercise