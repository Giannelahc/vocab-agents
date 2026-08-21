# schemas/preference.py
from pydantic import BaseModel

class LanguageDto(BaseModel):
    id: int
    code: str
    name: str

class UserPreferenceDto(BaseModel):
    id: int | None = None
    native_language: LanguageDto
    learning_languages: list[LanguageDto]
