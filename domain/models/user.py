#domain/models/user.py
from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional

@dataclass
class User:

    id: Optional[int]
    name: str
    lastname: str
    username: str
    email: str
    password_hash: str
    streak: int
    last_streak_date: date | None
    created_at: Optional[datetime] = None