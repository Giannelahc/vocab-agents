# schemas/preference.py
from pydantic import BaseModel

class LanguageDto(BaseModel):
    id: int
    code: str
    name: str

class UserPreferenceDto(BaseModel):
    id: int | None = None
    native_language: LanguageDto | None = None
    learning_languages: list[LanguageDto] = []

class UserPreferenceRequest(BaseModel):
    id: int | None = None
    native_language_id: int
    learning_languages_ids: list[int]
