
# infrastructure/security/jwt_service.py

from datetime import datetime, timedelta, timezone

import jwt

from config import settings


class JWTService:

    def create_access_token(self, user_id: int) -> str:

        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        payload = {
            "sub": str(user_id),
            "exp": expire,
            "iat": datetime.now(timezone.utc)
        }

        token = jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )

        return token
    
    def decode_token(self, token: str) -> dict:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return int(payload["sub"])