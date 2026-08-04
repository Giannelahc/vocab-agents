# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    OPENAI_API_KEY: str
    SERP_API_KEY:   str
    SECRET_KEY:     str
    ALGORITHM:      str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    INTERVALS: list[int] = [1, 3, 7, 14, 30, 60]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()