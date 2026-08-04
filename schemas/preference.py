# schemas/preference.py
from pydantic import BaseModel

class UserPreferenceRequest(BaseModel):
    id: int | None = None
    native_language_id: int
    learning_languages: list[int]
