
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from domain.models.user import User
from domain.repositories.user_repository import UserRepository
from infrastructure.persistence.entities.user import UserModel
from infrastructure.persistence.mappers.user_mapper import UserMapper


class SQLUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user: User) -> User:
        model = UserMapper.to_model(user)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return UserMapper.to_entity(model)


    async def find_by_id(self, user_id: int) -> User | None:

        stmt = select(UserModel).where(
            UserModel.id == user_id
        )

        result = await self.session.execute(stmt)

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return UserMapper.to_entity(model)

    async def find_by_email(self, email: str) -> User | None:
        stmt = select(UserModel).where(
            UserModel.email == email
        )

        result = await self.session.execute(stmt)

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return UserMapper.to_entity(model)
    
    async def find_by_username(self, username: str) -> User | None:
        stmt = select(UserModel).where(
            UserModel.username == username
        )

        result = await self.session.execute(stmt)

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return UserMapper.to_entity(model)
