from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from core.config import settings

class Connection:
    _instance = None
    _engine = None
    _session_factory = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Connection, cls).__new__(cls, *args, **kwargs)
            cls._engine = create_async_engine(
                settings.DATABASE_URL,
                echo=True,
            )
            cls._session_factory = sessionmaker(
                bind=cls._engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
        return cls._instance

    async def get_session(self):
        async with self._session_factory() as session:
            yield session

    async def close(self):
        await self._engine.dispose()

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with Connection()._session_factory() as session:
            yield session
