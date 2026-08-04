from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from config import settings


DATABASE_URL = settings.DATABASE_URL
if DATABASE_URL.startswith("postgresql+psycopg2://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql+psycopg2://", "postgresql+asyncpg://", 1)

engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)
Base = declarative_base()

import entities.language
import entities.user
import entities.user_preferences
import entities.user_learning_language
import entities.vocabulary_word
import entities.word_sense
import entities.example
import entities.user_example

async def init_db():
    """
    Creates all tables defined in models that inherit from Base.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db