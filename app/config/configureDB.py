import contextlib
from typing import Any, AsyncIterator
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base
from app import config


class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}):
        self.__engine = create_async_engine(host, **engine_kwargs)
        self.sessionmaker = async_sessionmaker(
            autocommit=False, bind=self.__engine)

    async def close(self):
        if self.__engine is None:
            raise Exception("DatabaseSessionManager não iniciado")
        await self.__engine.dispose()

        self.__engine = None
        self.sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self.__engine is None:
            raise Exception("DatabaseSessionManager não iniciado")

        async with self.__engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self.sessionmaker is None:
            raise Exception("DatabaseSessionManager não iniciado")

        session = self.sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_db_session():
    async with sessionmanager.session() as session:
        yield session

Base = declarative_base()

sessionmanager = DatabaseSessionManager(
    config.settings.database_url, {"echo": config.settings.echo_sql})
