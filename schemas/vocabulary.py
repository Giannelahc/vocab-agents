# schemas/vocabulary.py
from pydantic import BaseModel

class VocabularyRequest(BaseModel):
    word: str
    language_id: int

class ExampleResponse(BaseModel):
    id: int
    sentence: str

class ExampleRequest(BaseModel):
    examples: list[str]

class SynonymResponse(BaseModel):
    id: int
    word: str

class UserExampleResponse(BaseModel):
    id: int
    sentence: str

class WordSenseResponse(BaseModel):
    id: int
    grammar_type: str
    definition: str
    translations: dict[str, list[str]]
    conjugation: dict | None = None
    gender: str | None = None
    examples: list[ExampleResponse] 
    synonyms: list[SynonymResponse] 
    user_examples: list[UserExampleResponse] | None = None

class VocabularyWordResponse(BaseModel):
    id: int
    word: str
    language_id: int
    status: str
    senses: list[WordSenseResponse]