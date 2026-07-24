#domain/models/user.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:

    id: Optional[int]
    name: str
    lastname: str
    username: str
    email: str
    password_hash: str
    created_at: Optional[datetime] = None