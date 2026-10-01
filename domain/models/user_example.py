#domain/models/user_example.py
from dataclasses import dataclass
from typing import Optional
    
@dataclass
class UserExample:

    user_vocabulary_id: int
    word_sense_id: int
    sentence: str
    id: Optional[int] = None