from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from api import auth_controller, vocabulary_controller, preference_controller, review_controller
from infrastructure.persistence.database import AsyncSessionLocal, init_db
from infrastructure.initializers.language_initializer import LanguageInitializer
from infrastructure.repositories.sql_language_repository import SQLLanguageRepository
from core.container import http_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()

    async with AsyncSessionLocal() as session:
        repository = SQLLanguageRepository(session)

        initializer = LanguageInitializer(repository)

        await initializer.initialize()

    yield
    await http_client.close()

app = FastAPI(title="Vocabulary API", lifespan=lifespan)

app.include_router(auth_controller.router, prefix="/vocan-agent/auth", tags=["Auth"])
app.include_router(vocabulary_controller.router, prefix="/vocan-agent/vocabulary", tags=["Vocabulary"])
app.include_router(preference_controller.router, prefix="/vocan-agent/preference", tags=["Preference"])
app.include_router(review_controller.router, prefix="/vocan-agent/reviews", tags=["Review"])