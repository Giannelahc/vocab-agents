# schemas/vocabulary.py
from pydantic import BaseModel

class VocabularyRequest(BaseModel):
    word: str
    language_id: int
