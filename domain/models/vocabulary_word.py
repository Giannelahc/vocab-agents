#domain/models/vocabulary_word.py
from dataclasses import dataclass, field
from typing import Optional
from domain.models.word_sense import WordSense
from application.enums.vocabulary_status import VocabularyStatus
    
@dataclass
class VocabularyWord:

    word: str
    language_id: int
    status: VocabularyStatus = VocabularyStatus.PENDING
    senses: list[WordSense] = field(default_factory=list)
    id: Optional[int] = None