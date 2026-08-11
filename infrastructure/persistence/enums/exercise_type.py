from enum import Enum


class ExerciseType(int, Enum):
    MULTIPLE_CHOICE_DEFINITION = 0
    MULTIPLE_CHOICE_TRANSLATION = 1
    FILL_IN_THE_BLANK = 2
    WORD_COMPLETION = 3
    OPEN_ANSWER = 4