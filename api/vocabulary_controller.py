

from fastapi import APIRouter, BackgroundTasks, Depends, status

from application.enums.vocabulary_status import VocabularyStatus
from application.services.supervisor_service import SupervisorService
from dependencies import get_current_user, get_supervisor_service
from schemas.vocabulary import VocabularyRequest

router = APIRouter()

@router.post("/register-word",
             status_code=status.HTTP_202_ACCEPTED)
async def create_word(
    request: VocabularyRequest,
    background_tasks: BackgroundTasks,
    user_id: int = Depends(get_current_user),
    service: SupervisorService = Depends(get_supervisor_service)
):
    vocabulary = await service.register_word(word=request.word, language_id=request.language_id, user_id=user_id)

    if vocabulary.status == VocabularyStatus.FAILED:
        background_tasks.add_task(service.process_word, user_id, vocabulary.id)

    return vocabulary
    
