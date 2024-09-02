"""
Use this module to register required services.
Services registered inside a `rodi.Container` are automatically injected into request
handlers.

For more information and documentation, see `rodi` Wiki and examples:
    https://github.com/Neoteroi/rodi/wiki
    https://github.com/Neoteroi/rodi/tree/main/examples
"""

from __future__ import annotations

from typing import Tuple

from rodi import Container


from xcov19.app.settings import Settings
from xcov19.services.geolocation import (
    LocationQueryServiceInterface,
    GeolocationQueryService,
)


def configure_services(settings: Settings) -> Tuple[Container, Settings]:
    container = Container()

    container.add_instance(settings)
    container.add_singleton(LocationQueryServiceInterface, GeolocationQueryService)

    return container, settings
