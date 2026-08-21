# schemas/user.py
from pydantic import BaseModel
from datetime import datetime
from schemas.preference import UserPreferenceDto


class UserInfoResponse(BaseModel):
    id: int
    name: str
    lastname: str
    username: str
    email: str
    created_at: datetime
    preference: UserPreferenceDto | None = None
