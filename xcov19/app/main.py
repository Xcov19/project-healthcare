"""
This module configures the BlackSheep application before it starts.
"""

from blacksheep import Application
from rodi import Container

from xcov19.app.auth import configure_authentication
from xcov19.app.docs import configure_docs
from xcov19.app.errors import configure_error_handlers
from xcov19.app.middleware import origin_header_middleware, configure_middleware
from xcov19.app.services import configure_services
from xcov19.app.settings import load_settings, Settings


def configure_application(
    services: Container,
    settings: Settings,
) -> Application:
    app = Application(
        services=services, show_error_details=settings.app.show_error_details
    )

    configure_error_handlers(app)
    configure_authentication(app, settings)
    configure_middleware(app, origin_header_middleware)
    configure_docs(app, settings)
    return app


app = configure_application(*configure_services(load_settings()))
