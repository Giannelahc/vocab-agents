
from domain.models.user import User
from infrastructure.persistence.entities.user import UserModel


class UserMapper:

    @staticmethod
    def to_entity(model: UserModel) -> User:

        return User(
            id=model.id,
            name=model.name,
            lastname=model.lastname,
            username=model.username,
            email=model.email,
            password_hash=model.password_hash,
            created_at=model.created_at
        )

    @staticmethod
    def to_model(entity: User) -> UserModel:

        return UserModel(
            id=entity.id,
            name=entity.name,
            lastname=entity.lastname,
            username=entity.username,
            email=entity.email,
            password_hash=entity.password_hash
        )