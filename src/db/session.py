from typing import Any, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.settings import settings


DATABASE_URL = (
    f"postgresql+asyncpg://{settings.postgres_user}:"
    f"{settings.postgres_password}"
    f"@{settings.postgres_host}:"
    f"{settings.postgres_port}/{settings.postgres_database_name}"
)


engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
Base = declarative_base()


async def get_session() -> AsyncGenerator[Any, AsyncSession]:
    async with async_session() as session:
        yield session
