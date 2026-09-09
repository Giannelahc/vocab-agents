
# application/services/auth_service.py

from pwdlib import PasswordHash

from domain.models.user import User
from domain.repositories.user_repository import UserRepository
from infrastructure.security.jwt_service import JWTService


password_hasher = PasswordHash.recommended()


class AuthService:

    def __init__(self, repository: UserRepository, jwt_service: JWTService):
        self.repository = repository
        self.jwt_service = jwt_service

    async def register(self, name: str, lastname: str, username: str, email: str, password: str) -> User:

        existing = await self.repository.find_by_email(email)

        if existing:
            raise ValueError("Email already exists")

        user = User(
            id=None,
            name=name,
            lastname=lastname,
            username=username,
            email=email,
            password_hash=password_hasher.hash(password)
        )

        user = await self.repository.save(user)

        return user

    async def login(self, email: str, password: str):
        user = await self.repository.find_by_email(email)

        if user is None:
            raise ValueError("Invalid credentials")

        if not password_hasher.verify(
            password,
            user.password_hash
        ):
            raise ValueError("Invalid credentials")

        token = self.jwt_service.create_access_token(
            user.id
        )

        return token

    async def logout(self, token: str) -> None:
        self.jwt_service.revoke_token(token)