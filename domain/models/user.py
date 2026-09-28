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
    streak: Optional[int] = None
    last_streak_date: Optional[date] = None
    created_at: Optional[datetime] = None