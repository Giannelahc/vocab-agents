

from fastapi import APIRouter, Depends

from dependencies import get_current_user, get_language_service
from api.mappers.user_preference_mapper import LanguageMapper
from application.services.language_service import LanguageService

router = APIRouter()

@router.get("")
async def get_languages(
    user_id: int = Depends(get_current_user),
    service: LanguageService = Depends(get_language_service)
):
    languages = await service.get_languages()
    return [LanguageMapper.to_request(language) for language in languages ]
    
