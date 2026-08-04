#domain/models/language.py
from dataclasses import dataclass
from typing import Optional
    
@dataclass
class Language:

    id: Optional[int]
    code: str
    name: str