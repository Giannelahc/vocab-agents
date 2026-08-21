#domain/models/user_info.py
from dataclasses import dataclass
from datetime import datetime
from domain.models.user_preference import UserPreference

@dataclass
class UserInfo:

    id: int
    name: str
    lastname: str
    username: str
    email: str
    created_at: datetime
    preference: UserPreference | None = None