# dependencies.py

from fastapi import Depends

from database import get_db

from infrastructure.repositories.sql_user_repository import (
    SQLUserRepository
)

from infrastructure.security.jwt_service import (
    JWTService
)

from application.services.auth_service import (
    AuthService
)

async def get_user_repository(session=Depends(get_db)):
    return SQLUserRepository(session)

def get_jwt_service():
    return JWTService()

def get_auth_service(repository=Depends(get_user_repository),
    jwt_service=Depends(get_jwt_service)):

    return AuthService(repository, jwt_service)