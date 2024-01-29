from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from backend.database.models.base import AlchemyBaseModel
from backend.settings import Settings


__factory: None | async_sessionmaker = None


async def database_init(settings: Settings) -> None:
    global __factory

    if __factory:
        return

    async_engine = create_async_engine(f"sqlite+aiosqlite:///{settings.db_path}")
    __factory = async_sessionmaker(
        bind=async_engine,
        autoflush=False,
        future=True,
        expire_on_commit=False,
    )

    async with async_engine.begin() as conn:
        await conn.run_sync(AlchemyBaseModel.metadata.create_all)


async def get_session() -> AsyncIterator[AsyncSession]:
    if not __factory:
        raise RuntimeError("Брат, а кто database_init вызывать будет?")

    async with __factory() as session:
        yield session
