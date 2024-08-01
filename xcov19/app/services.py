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

from xcov19.app.dto import Address, LocationQueryJSON, FacilitiesResult, GeoLocation
from xcov19.app.settings import Settings


def configure_services(settings: Settings) -> Tuple[Container, Settings]:
    container = Container()

    container.add_instance(settings)
    container.add_scoped(LocationQueryServiceInterface, GeolocationQueryServiceImpl)

    return container, settings


class LocationQueryServiceInterface[T: LocationQueryJSON](Protocol):
    """Location aware service for listing faciltiies.
    1. Searches and fetches existing for query_id for a cust_id
    2. Resolves coordinates from a given geolocation.
    3. Fetches all facilities from a given set of records for a
    given radius from geolocation.

    Radius is default for now.
    # TODO: Filter to be added
    """

    @classmethod
    @abc.abstractmethod
    async def resolve_coordinates(cls, query: T) -> Address:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    async def fetch_facilities(cls, query: T) -> FacilitiesResult:
        raise NotImplementedError


# TODO: make hard-coded response functional
class GeolocationQueryServiceImpl(LocationQueryServiceInterface):
    @classmethod
    async def resolve_coordinates(cls, query: LocationQueryJSON) -> Address:
        return Address()

    @classmethod
    async def fetch_facilities(cls, query: LocationQueryJSON) -> FacilitiesResult:
        return FacilitiesResult(
            name="Test facility",
            address=Address(),
            geolocation=GeoLocation(lat=0.0, lng=0.0),
            contact="+919999999999",
            facility_type="nursing",
            ownership="charity",
            specialties=["surgery", "pediatrics"],
            stars=4,
            reviews=120,
            rank=2,
            estimated_time=20,
        )
