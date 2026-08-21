# schemas/vocabulary.py
from pydantic import BaseModel
from schemas.preference import LanguageDto

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
    properties: dict | None = None
    gender: str | None = None
    examples: list[ExampleResponse] 
    synonyms: list[SynonymResponse] 
    user_examples: list[UserExampleResponse] | None = None

class VocabularyWordSummaryResponse(BaseModel):
    id: int
    word: str
    language: LanguageDto | None = None
    status: str
    senses: int = 0

class VocabularyWordResponse(BaseModel):
    id: int
    word: str
    language: LanguageDto | None = None
    status: str
    senses: list[WordSenseResponse]

class VocabularyCandidateResponse(BaseModel):
    text: str
    type: str
    base_form: str
    already_registered: bool

class VocabularyIdentifyRequest(BaseModel):
    text: str
    language_id: int

class VocabularyListResponse(BaseModel):
    page: int
    page_size: int
    total: int
    items: list[VocabularyWordSummaryResponse]