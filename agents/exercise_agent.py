from prompts.exercise_prompt import ExercisePromptBuilder
from application.enums.exercise_type import ExerciseType

class ExerciseAgent:
    def __init__(self, exercise_service: ExercisePromptBuilder):
        self.exercise_service = exercise_service

    def generate_exercises(self, exercise_type: ExerciseType, word: str, correct_answer: str, 
                           tag: str, target_language: str, native_language: str):
        match(exercise_type):
            case ExerciseType.MULTIPLE_CHOICE_DEFINITION:
                return self.exercise_service.generate_definition_exercise(word, tag, target_language, 
                                                                          correct_definition=correct_answer)
            case ExerciseType.MULTIPLE_CHOICE_TRANSLATION:
                return self.exercise_service.generate_multiple_choice_translation_exercise(word, tag, native_language, 
                                                                                           correct_translation=correct_answer)
            case ExerciseType.FILL_IN_THE_BLANK:
                return self.exercise_service.generate_fill_in_the_blank_exercise(word, tag, target_language, 
                                                                                 synonym=correct_answer)
            case ExerciseType.WORD_COMPLETION:
                # Implementation for word completion exercise
                pass
            case ExerciseType.OPEN_ANSWER:
                # Implementation for open answer exercise
                pass