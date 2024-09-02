"""
This module configures the BlackSheep application before it starts.
"""

from blacksheep import Application
from rodi import Container, ContainerProtocol

from xcov19.app.database import (
    configure_database_session,
    setup_database,
    start_db_session,
)
from xcov19.app.auth import configure_authentication
from xcov19.app.controllers import controller_router
from xcov19.app.docs import configure_docs
from xcov19.app.errors import configure_error_handlers
from xcov19.app.middleware import origin_header_middleware, configure_middleware
from xcov19.app.services import configure_services
from xcov19.app.settings import load_settings, Settings

from sqlalchemy.ext.asyncio import AsyncEngine


def configure_application(
    services: Container,
    settings: Settings,
) -> Application:
    app = Application(
        services=services, show_error_details=settings.app.show_error_details
    )
    app.controllers_router = controller_router

    configure_error_handlers(app)
    configure_authentication(app, settings)
    configure_middleware(app, origin_header_middleware)
    configure_docs(app, settings)
    configure_database_session(services, settings)
    return app


app = configure_application(*configure_services(load_settings()))


@app.on_start
async def on_start():
    container: ContainerProtocol = app.services
    if not isinstance(container, Container):
        raise ValueError("Container is not a valid container")
    await start_db_session(container)
    engine = container.resolve(AsyncEngine)
    await setup_database(engine)
