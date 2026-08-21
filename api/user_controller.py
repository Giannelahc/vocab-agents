

from fastapi import APIRouter, Depends

from dependencies import get_current_user, get_use_service
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

    
