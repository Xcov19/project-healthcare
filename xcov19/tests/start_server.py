from collections.abc import AsyncGenerator
from blacksheep import Application
from contextlib import AsyncExitStack, asynccontextmanager
from rodi import Container, ContainerProtocol
from xcov19.app.database import (
    configure_database_session,
    setup_database,
    start_db_session,
)
from xcov19.app.settings import load_settings
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlmodel.ext.asyncio.session import AsyncSession as AsyncSessionWrapper


class InvalidSessionTypeError(RuntimeError):
    """Exception raised when the session is not of the expected type."""

    pass


class InvalidDIContainerTypeError(RuntimeError):
    """Exception raised when valid DI container not found."""

    pass


@asynccontextmanager
async def start_server(app: Application) -> AsyncGenerator[Application, None]:
    """Start a test server for automated testing."""
    try:
        await app.start()
        yield app
    finally:
        if app.started:
            await app.stop()


class SetUpTestDatabase:
    """Manages the lifecycle of the test database."""

    def __init__(self) -> None:
        self._stack = AsyncExitStack()
        self._session: AsyncSession | AsyncSessionWrapper | None = None
        self._container: ContainerProtocol = Container()

    async def setup_test_database(self) -> None:
        """Database setup for integration tests."""
        if not isinstance(self._container, Container):
            raise InvalidDIContainerTypeError("Container not of valid type.")
        configure_database_session(self._container, load_settings())
        engine = self._container.resolve(AsyncEngine)
        await setup_database(engine)

    async def start_async_session(self) -> AsyncSession | AsyncSessionWrapper:
        """Returns an asynchronous session."""
        if not isinstance(self._container, Container):
            raise InvalidDIContainerTypeError("Container not of valid type.")
        self._session = await self._stack.enter_async_context(
            start_db_session(self._container)
        )
        if not isinstance(self._session, AsyncSessionWrapper):
            raise InvalidSessionTypeError(
                f"{self._session} is not a AsyncSessionWrapper value."
            )
        return self._session

    async def aclose(self) -> None:
        # TODO: replace print with logger
        print("async closing test server db session closing.")
        if not isinstance(self._session, AsyncSessionWrapper):
            raise InvalidSessionTypeError(
                f"{self._session} is not a AsyncSessionWrapper value."
            )
        await self._session.commit()
        await self._stack.aclose()
        print("async test server closing.")
