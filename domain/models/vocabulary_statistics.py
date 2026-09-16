from dataclasses import dataclass


@dataclass
class VocabularyStatistics:

    language_id: int
    language_name: str
    learned_words: int
    total_words: int
    new_words_current_week: int

