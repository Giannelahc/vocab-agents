#domain/models/user_example.py
from dataclasses import dataclass
from typing import Optional
    
@dataclass
class UserExample:

    id: Optional[int]
    sentence: str