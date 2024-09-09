from collections.abc import AsyncGenerator
from blacksheep import Application
from contextlib import asynccontextmanager
from rodi import Container, ContainerProtocol
from xcov19.app.database import configure_database_session, setup_database
from xcov19.app.settings import load_settings
from sqlalchemy.ext.asyncio import AsyncEngine


@asynccontextmanager
async def start_server(app: Application) -> AsyncGenerator[Application, None]:
    """Start a test server for automated testing."""
    try:
        await app.start()
        yield app
    finally:
        if app.started:
            await app.stop()


async def start_test_database(container: ContainerProtocol) -> None:
    """Database setup for integration tests."""
    if not isinstance(container, Container):
        raise RuntimeError("container not of type Container.")
    configure_database_session(container, load_settings())
    engine = container.resolve(AsyncEngine)
    await setup_database(engine)
