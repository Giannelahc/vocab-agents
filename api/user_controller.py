

from sqlalchemy import text
import time

from infrastructure.persistence.database import engine

from fastapi import APIRouter, Depends

from api.mappers.home_info_mapper import HomeInfoMapper
from application.services.home_service import HomeService
from dependencies import get_current_user, get_home_service, get_use_service
from api.mappers.user_info_mapper import UserInfoMapper
from application.services.user_service import UserService

router = APIRouter()

@router.get("/me")
async def get_user_info(
    user_id: int = Depends(get_current_user),
    service: UserService = Depends(get_use_service)
):
    user_info = await service.get_user_info(user_id)
    return UserInfoMapper.to_response(user_info)

@router.get("/home-summary")
async def get_home_summary(
    user_id: int = Depends(get_current_user),
    service: HomeService = Depends(get_home_service)
):
    home_info = await service.get_home_summary(user_id)
    return HomeInfoMapper.to_response(home_info)


@router.get("/db-test")
async def db_test():
    start = time.perf_counter()

    async with engine.connect() as conn:
        connection_time = time.perf_counter() - start

        start_query = time.perf_counter()
        await conn.execute(text("select * from public.users where id = 4"))
        await conn.execute(text("select * from public.user_preferences up inner join public.languages l on up.native_language_id = l.id"))
        query_time = time.perf_counter() - start_query

    return {
        "connection_seconds": round(connection_time, 3),
        "query_seconds": round(query_time, 3),
    }