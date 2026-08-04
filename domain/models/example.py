#domain/models/vocabulary_word.py
from dataclasses import dataclass
from typing import Optional
    
@dataclass
class Example:

    sentence: str
    id: Optional[int] = None