

from fastapi import APIRouter, Depends

from dependencies import get_current_user, get_user_preference_service
from api.mappers.user_preference_mapper import UserPreferenceMapper
from schemas.preference import UserPreferenceDto
from application.services.user_preference import UserPreferenceService

router = APIRouter()

@router.post("/")
async def register_preference(
    request: UserPreferenceDto,
    user_id: int = Depends(get_current_user),
    service: UserPreferenceService = Depends(get_user_preference_service)
):
    user_preference = UserPreferenceMapper.to_entity(request, user_id)
    saved_preference = await service.save_user_preferences(user_preference)
    return UserPreferenceMapper.to_dto(saved_preference)

@router.get("/")
async def get_preference(
    user_id: int = Depends(get_current_user),
    service: UserPreferenceService = Depends(get_user_preference_service)
):
    user_preference = await service.get_user_preferences(user_id)
    return UserPreferenceMapper.to_dto(user_preference)
    
