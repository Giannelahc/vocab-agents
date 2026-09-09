
# infrastructure/security/jwt_service.py

from datetime import datetime, timedelta, timezone

import jwt

from core.config import settings


class JWTService:

    revoked_tokens = set()

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

    def revoke_token(self, token: str) -> None:
        if token:
            JWTService.revoked_tokens.add(token)

    def is_token_revoked(self, token: str) -> bool:
        return token in JWTService.revoked_tokens

    def decode_token(self, token: str) -> dict:
        if self.is_token_revoked(token):
            raise ValueError("Token has been revoked")

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return int(payload["sub"])
