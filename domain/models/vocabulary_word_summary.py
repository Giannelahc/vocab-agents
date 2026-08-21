#domain/models/vocabulary_word_summary.py
from dataclasses import dataclass, field
from typing import Optional
from domain.models.language import Language
from application.enums.vocabulary_status import VocabularyStatus
    
@dataclass
class VocabularyWordSummary:

    word: str
    language_id: int
    senses: int = 0
    language: Optional[Language] = None
    status: VocabularyStatus = VocabularyStatus.PENDING
    id: Optional[int] = None