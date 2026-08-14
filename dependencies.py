# dependencies.py

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from agents.definition_agent import DefinitionAgent
from agents.example_agent import ExampleAgent
from agents.grammar_agent import GrammarAgent
from agents.exercise_agent import ExerciseAgent
from agents.supervisor_agent import SupervisorAgent
from agents.vocabulary_identification_agent import VocabularyIdentificationAgent
from application.services.supervisor_service import SupervisorService
from application.services.vocabulary_word_service import VocabularyWordService
from application.services.user_example_service import UserExampleService
from application.services.review_service import ReviewService
from application.services.vocabulary_identifier_service import VocabularyIdentifierService
from infrastructure.persistence.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from domain.repositories.vocabulary_word_repository import VocabularyWordRepository
from domain.repositories.user_vocabulary_repository import UserVocabularyRepository
from domain.repositories.language_repository import LanguageRepository
from domain.repositories.review_repository import ReviewRepository
from domain.repositories.user_example_repository import UserExampleRepository

from infrastructure.clients.llm_client import LLMClient
from infrastructure.repositories.sql_language_repository import SQLLanguageRepository
from infrastructure.repositories.sql_user_preference_repository import SQLUserPreferenceRepository
from infrastructure.repositories.sql_user_vocabulary_repository import SQLUserVocabularyRepository
from infrastructure.repositories.sql_user_repository import SQLUserRepository
from infrastructure.repositories.sql_review_repository import SQLReviewRepository
from infrastructure.repositories.sql_user_example_repository import SQLUserExampleRepository

from infrastructure.repositories.sql_vocabulary_word_repository import SQLVocabularyWordRepository
from infrastructure.security.jwt_service import JWTService

from application.services.auth_service import AuthService
from application.mappers.vocabulary_mapper import VocabularyMapper
from application.mappers.review_mapper import ReviewMapper

from core.container import serp_api_client
from core.container import openai_client

from prompts.definition_prompt import DefinitionPromptBuilder
from prompts.example_prompt import ExamplePromptBuilder
from prompts.grammar_prompt import GrammarPromptBuilder
from prompts.pos_tagger_prompt import PosTaggerPromptBuilder
from prompts.exercise_prompt import ExercisePromptBuilder
from prompts.vocabulary_identification_prompt import VocabularyIdentificationPromptBuilder
from application.services.user_preference import UserPreferenceService

async def get_user_repository(session=Depends(get_db)):
    return SQLUserRepository(session)

def get_jwt_service():
    return JWTService()

def get_llm_client():
    return openai_client

def get_serapi_client():
    return serp_api_client

def get_auth_service(repository=Depends(get_user_repository),
    jwt_service=Depends(get_jwt_service)):

    return AuthService(repository, jwt_service)

def get_vocabulary_repository(session=Depends(get_db)):
    return SQLVocabularyWordRepository(session)

def get_user_vocabulary_repository(session=Depends(get_db)):
    return SQLUserVocabularyRepository(session)

def get_language_repository(session=Depends(get_db)):
    return SQLLanguageRepository(session)

def get_user_preference_repository(session=Depends(get_db)):
    return SQLUserPreferenceRepository(session)

def get_review_repository(session=Depends(get_db)):
    return SQLReviewRepository(session)

def get_user_example_repository(session=Depends(get_db)):
    return SQLUserExampleRepository(session)

def get_user_preference_service(user_preference_repository=Depends(get_user_preference_repository)):
    return UserPreferenceService(user_preference_repository)

def get_definition_prompt_builder():
    return DefinitionPromptBuilder(
        llm_client=get_llm_client(),
        serapi_client=get_serapi_client()
    )

def get_grammar_service():
    return GrammarPromptBuilder(llm_client=get_llm_client())

def get_example_service():
    return ExamplePromptBuilder(
        llm_client=get_llm_client(),
        serapi_client=get_serapi_client()
    )

def get_exercise_service():
    return ExercisePromptBuilder(llm_client=get_llm_client())

def get_vocabulary_identification_builder():
    return VocabularyIdentificationPromptBuilder(llm_client=get_llm_client())

def get_definition_agent():
    return DefinitionAgent(dictionary_service=get_definition_prompt_builder())

def get_grammar_agent():
    return GrammarAgent(grammar_service=get_grammar_service())

def get_example_agent():
    return ExampleAgent(example_service=get_example_service())

def get_exercise_agent():
    return ExerciseAgent(exercise_service=get_exercise_service())

def get_vocabulary_identification_agent():
    return VocabularyIdentificationAgent(vocabulary_identify_builder=get_vocabulary_identification_builder())

def get_pos_tagger_service():
    return PosTaggerPromptBuilder(llm_client=get_llm_client())

def get_supervisor_agent():
    return SupervisorAgent(definition_agent=get_definition_agent(), grammar_agent=get_grammar_agent(),
                           example_agent=get_example_agent(), pos_tagger=get_pos_tagger_service())

def get_review_service(
        session: AsyncSession = Depends(get_db),
        review_repository: ReviewRepository = Depends(get_review_repository),    
        user_vocabulary_repository: UserVocabularyRepository = Depends(get_user_vocabulary_repository),
        vocabulary_repository: VocabularyWordRepository = Depends(get_vocabulary_repository),
        language_repository: LanguageRepository = Depends(get_language_repository),
        user_preference_service: UserPreferenceService = Depends(get_user_preference_service),
        exercise_agent: ExerciseAgent = Depends(get_exercise_agent)) -> ReviewService:
    return ReviewService(
        session=session,
        review_repository=review_repository,
        user_vocabulary_repository=user_vocabulary_repository,
        vocabulary_word_repository=vocabulary_repository,
        language_repository=language_repository,
        user_preference_service=user_preference_service,
        exercise_agent=exercise_agent,
        review_mapper=ReviewMapper()
    )

def get_supervisor_service(
    session: AsyncSession = Depends(get_db),
    vocabulary_repository: VocabularyWordRepository = Depends(get_vocabulary_repository),
    user_vocabulary_repository: UserVocabularyRepository = Depends(get_user_vocabulary_repository),
    language_repository: LanguageRepository = Depends(get_language_repository),
    user_preference_service: UserPreferenceService = Depends(get_user_preference_service),
    review_service: ReviewService = Depends(get_review_service),
    supervisor_agent: SupervisorAgent = Depends(get_supervisor_agent),
) -> SupervisorService:

    return SupervisorService(
        session=session,
        vocabulary_repository=vocabulary_repository,
        user_vocabulary_repository=user_vocabulary_repository,
        language_repository=language_repository,
        review_service=review_service,
        user_preference_service=user_preference_service,
        supervisor_agent=supervisor_agent,
        vocabulary_mapper=VocabularyMapper()
    )

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

def get_current_user(token: str = Depends(oauth2_scheme)):

    user_id = get_jwt_service().decode_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return user_id

def get_vocabulary_word_service(
    vocabulary_word_repository: VocabularyWordRepository = Depends(get_vocabulary_repository)
) -> VocabularyWordService:
    return VocabularyWordService(vocabulary_word_repository=vocabulary_word_repository)

def get_user_example_service(
    user_example_repository: UserExampleRepository = Depends(get_user_example_repository)
) -> UserExampleService:
    return UserExampleService(user_example_repository=user_example_repository)

def get_vocabulary_identification_service(
        vocabulary_identification_agent: VocabularyIdentificationAgent = Depends(get_vocabulary_identification_agent),
        language_repository: LanguageRepository = Depends(get_language_repository),
        vocabulary_word_repository: VocabularyWordRepository = Depends(get_vocabulary_repository)
) -> VocabularyIdentifierService:
    return VocabularyIdentifierService(vocabulary_word_repository= vocabulary_word_repository,
                                       language_repository= language_repository,
                                       identification_agent= vocabulary_identification_agent)
