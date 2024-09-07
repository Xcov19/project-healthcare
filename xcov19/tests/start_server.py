from collections.abc import AsyncGenerator
from xcov19.app.main import app
from blacksheep import Application


async def start_server() -> AsyncGenerator[Application, None]:
    """Start a test server for automated testing."""
    try:
        await app.start()
        yield app
    finally:
        if app.started:
            await app.stop()
