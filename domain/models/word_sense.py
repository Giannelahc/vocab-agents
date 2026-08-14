#domain/models/word_sense.py
from dataclasses import dataclass, field
from typing import Optional
from domain.models.example import Example
from domain.models.synonym import Synonym
from domain.models.user_example import UserExample
    
@dataclass
class WordSense:

    grammar_type: str
    definition: str
    id: Optional[int] = None
    translations: Optional[dict[str, list[str]]] = None
    conjugation: Optional[dict] = None
    properties: Optional[dict] = None
    gender: Optional[str] = None
    examples: list[Example] = field(default_factory=list)
    synonyms: list[Synonym] = field(default_factory=list)
    user_examples: list[UserExample] = field(default_factory=list)