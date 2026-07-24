# schemas/auth.py
from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    name: str
    lastname: str
    username: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str