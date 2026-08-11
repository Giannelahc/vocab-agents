

from fastapi import APIRouter, BackgroundTasks, Depends, Query, status

from application.enums.vocabulary_status import VocabularyStatus
from application.services.supervisor_service import SupervisorService
from application.services.vocabulary_word_service import VocabularyWordService
from dependencies import get_current_user, get_supervisor_service, get_vocabulary_word_service
from schemas.vocabulary import VocabularyRequest

router = APIRouter()

@router.post("/register-word",
             status_code=status.HTTP_202_ACCEPTED)
async def create_word(
    request: VocabularyRequest,
    background_tasks: BackgroundTasks,
    regenerate: bool = Query(False),
    user_id: int = Depends(get_current_user),
    service: SupervisorService = Depends(get_supervisor_service)
):
    vocabulary = await service.register_word(word=request.word, language_id=request.language_id, user_id=user_id)

    if regenerate or vocabulary.status == VocabularyStatus.FAILED or vocabulary.status == VocabularyStatus.PENDING:
        background_tasks.add_task(service.process_word, user_id, vocabulary.id)

    return vocabulary

@router.get("/")
async def get_vocabulary_paginated_by_language(
    language_id: int | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    user_id: int = Depends(get_current_user),
    service: VocabularyWordService = Depends(get_vocabulary_word_service)
):
    return await service.get_words_by_user(user_id, language_id, page, page_size)
    
