
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

    def create_refresh_token(self, user_id: int) -> str:
        expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        payload = {
            "sub": str(user_id),
            "exp": expire,
            "iat": datetime.now(timezone.utc),
            "type": "refresh"
        }

        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )

    def refresh_access_token(self, refresh_token: str) -> str:
        payload = jwt.decode(
            refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        if payload.get("type") != "refresh":
            raise ValueError("Invalid refresh token")

        if self.is_token_revoked(refresh_token):
            raise ValueError("Refresh token has been revoked")

        return self.create_access_token(int(payload["sub"]))

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
