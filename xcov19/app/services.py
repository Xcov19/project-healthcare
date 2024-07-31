"""
Use this module to register required services.
Services registered inside a `rodi.Container` are automatically injected into request
handlers.

For more information and documentation, see `rodi` Wiki and examples:
    https://github.com/Neoteroi/rodi/wiki
    https://github.com/Neoteroi/rodi/tree/main/examples
"""

import abc
from typing import Protocol, Tuple

from rodi import Container

from xcov19.app.dto import Address, LocationQueryJSON
from xcov19.app.settings import Settings


def configure_services(settings: Settings) -> Tuple[Container, Settings]:
    container = Container()

    container.add_instance(settings)
    container.add_scoped(LocationQueryServiceInterface, GeolocationQueryService)

    return container, settings


class LocationQueryServiceInterface[T: LocationQueryJSON](Protocol):
    @abc.abstractmethod
    async def resolve_coordinates(self, query: T) -> Address:
        raise NotImplementedError


class GeolocationQueryService(LocationQueryServiceInterface):
    async def resolve_coordinates(self, query: LocationQueryJSON) -> Address:
        return Address()
