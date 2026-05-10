from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class DatabaseService:
    def __init__(
        self,
        database_url: str,
        *,
        echo: bool = False,
        pool_size: int | None = None,
        max_overflow: int | None = None,
        pool_pre_ping: bool = True,
    ) -> None:
        engine_kwargs: dict[str, object] = {
            "echo": echo,
            "pool_pre_ping": pool_pre_ping,
        }

        if pool_size is not None:
            engine_kwargs["pool_size"] = pool_size

        if max_overflow is not None:
            engine_kwargs["max_overflow"] = max_overflow

        self._engine = create_async_engine(database_url, **engine_kwargs)
        self._session_factory = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @property
    def engine(self) -> AsyncEngine:
        return self._engine

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        return self._session_factory

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self._session_factory() as session:
            yield session

    async def dispose(self) -> None:
        await self._engine.dispose()
