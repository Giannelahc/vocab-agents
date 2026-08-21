

from fastapi import APIRouter, BackgroundTasks, Depends, Query, status

from application.enums.vocabulary_status import VocabularyStatus
from application.services.supervisor_service import SupervisorService
from application.services.vocabulary_word_service import VocabularyWordService
from application.services.user_example_service import UserExampleService
from application.services.vocabulary_identifier_service import VocabularyIdentifierService
from dependencies import get_current_user, get_supervisor_service, get_vocabulary_word_service, get_user_example_service, get_vocabulary_identification_service
from schemas.vocabulary import VocabularyRequest, ExampleRequest, VocabularyIdentifyRequest
from api.mappers.vocabulary_mapper import VocabularyMapper, UserExampleMapper
from api.mappers.vocabulary_candidate_mapper import VocabularyCandidateMapper

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
    vocabulary, review = await service.register_word(word=request.word, language_id=request.language_id, 
                                                     user_id=user_id, regenerate=regenerate)

    if regenerate or vocabulary.status == VocabularyStatus.FAILED or vocabulary.status == VocabularyStatus.PENDING:
        background_tasks.add_task(service.process_word, user_id, vocabulary.id, review)

    return VocabularyMapper.to_vocabulary_word_summary_response(vocabulary)

@router.get("")
async def get_vocabulary_paginated_by_language(
    language_id: int | None = Query(None),
    search: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    user_id: int = Depends(get_current_user),
    service: VocabularyWordService = Depends(get_vocabulary_word_service)
):
    vocabulary_list, total = await service.get_words_by_user(user_id, language_id, page, page_size, search)
    return VocabularyMapper.to_vocabulary_list_response(vocabulary_list, page, page_size, total)

@router.get("/{word_id}")
async def get_vocabulary_by_id(
    word_id: int,
    user_id: int = Depends(get_current_user),
    service: VocabularyWordService = Depends(get_vocabulary_word_service)
):
    vocabulary_word = await service.get_word_by_id(word_id)
    return VocabularyMapper.to_response(vocabulary_word)


@router.post("/{word_sense_id}/examples")
async def register_user_examples(
    user_examples: ExampleRequest,
    word_sense_id: int,
    user_id: int = Depends(get_current_user),
    service: UserExampleService = Depends(get_user_example_service)
):
    examples = await service.save_examples(user_examples.examples, word_sense_id)
    return [UserExampleMapper.to_response(example) for example in examples]


@router.post("/identify")
async def identify_vocabulary(
    request: VocabularyIdentifyRequest,
    user_id: int = Depends(get_current_user),
    service: VocabularyIdentifierService = Depends(
        get_vocabulary_identification_service
    )
):
    candidates = await service.identify(
        text=request.text,
        language_id=request.language_id,
        user_id=user_id
    )

    return [
        VocabularyCandidateMapper.to_response(candidate)
        for candidate in candidates
    ]
