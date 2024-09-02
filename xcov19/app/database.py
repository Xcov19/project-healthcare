from collections.abc import AsyncGenerator
import sys
from rodi import Container
from sqlmodel import SQLModel

from xcov19.app.settings import Settings
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)

import logging
from sqlalchemy.pool import AsyncAdaptedQueuePool

db_logger = logging.getLogger(__name__)
db_fmt = logging.Formatter(
    "DATABASE:%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(db_fmt)

db_logger.setLevel(logging.INFO)
db_logger.addHandler(stream_handler)


class SessionFactory:
    """Class to remember sessionmaker factory constructor for DI container.

    Use like this to retrieve sessionmaker from DI container:
    container.resolve(SessionFactory)

    It is already added as in `configure_database_session`:
    container.add_singleton_by_factory(SessionFactory(engine), SessionFactory)
    """

    def __init__(self, engine: AsyncEngine):
        self._engine = engine

    def __call__(self) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            self._engine, class_=AsyncSession, expire_on_commit=False
        )


async def setup_database(engine: AsyncEngine) -> None:
    """Sets up tables for database."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def create_async_session(
    AsyncSessionFactory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    """Create an asynchronous database session."""
    async with AsyncSessionFactory() as session:
        try:
            yield session
        finally:
            await session.close()


async def start_db_session(container: Container):
    """Starts a new database session given SessionFactory."""
    # add LocalAsyncSession
    local_async_session = create_async_session(
        container.resolve(async_sessionmaker[AsyncSession])
    )
    container.add_instance(local_async_session, AsyncSession)


def configure_database_session(container: Container, settings: Settings) -> Container:
    """Configure database session setup for the application."""
    # add engine
    db_logger.info(f"""====== Configuring database session. ======
                   DB_ENGINE_URL: {settings.db_engine_url}
                   """)
    engine = create_async_engine(
        settings.db_engine_url, echo=True, poolclass=AsyncAdaptedQueuePool
    )
    container.add_instance(engine, AsyncEngine)

    # add sessionmaker
    container.add_singleton_by_factory(
        SessionFactory(engine), async_sessionmaker[AsyncSession]
    )

    db_logger.info("====== Database session configured. ======")
    return container
