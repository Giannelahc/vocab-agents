from enum import Enum

class VocabularyType(str, Enum):
    VERB = "verb"
    VERBAL_EXPRESSION = "verbal_expression"
    NOUN = "noun"
    ADJECTIVE = "adjective"
    ADVERB = "adverb"
    IDIOM = "idiom"
    EXPRESSION = "expression"
    OTHER = "other"