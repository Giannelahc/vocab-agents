#domain/models/user_example.py
from dataclasses import dataclass
from typing import Optional
    
@dataclass
class UserExample:

    word_sense_id: int
    sentence: str
    id: Optional[int] = None