# schemas/preference.py
from pydantic import BaseModel

class UserPreferenceDto(BaseModel):
    id: int | None = None
    native_language_id: int
    learning_languages: list[int]
