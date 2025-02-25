from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from core.config import settings

class Connection:
    # Singleton instance variables
    _instance = None
    _engine = None
    _session_factory = None

    def __new__(cls, *args, **kwargs):
        # Implementing Singleton pattern to ensure only one instance
        if not cls._instance:
            cls._instance = super(Connection, cls).__new__(cls, *args, **kwargs)
            # Create an asynchronous engine using the database URL from settings
            cls._engine = create_async_engine(
                settings.DATABASE_URL,
                echo=True,  # Enable SQLAlchemy logging
            )
            # Create a session factory bound to the engine
            cls._session_factory = sessionmaker(
                bind=cls._engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
        return cls._instance

    async def get_session(self):
        # Provide an asynchronous session generator
        async with self._session_factory() as session:
            yield session

    async def close(self):
        # Dispose of the engine to close all connections
        await self._engine.dispose()

# Function to get a session, used outside the Connection class
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with Connection()._session_factory() as session:
        yield session
