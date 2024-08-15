"""
Use this module to register required services.
Services registered inside a `rodi.Container` are automatically injected into request
handlers.

For more information and documentation, see `rodi` Wiki and examples:
    https://github.com/Neoteroi/rodi/wiki
    https://github.com/Neoteroi/rodi/tree/main/examples
"""

import abc
from collections.abc import Callable
from typing import Protocol, Tuple, List

from rodi import Container

from xcov19.app.dto import Address, LocationQueryJSON, FacilitiesResult
from xcov19.app.settings import Settings
from xcov19.utils.mixins import InterfaceProtocolCheckMixin


def configure_services(settings: Settings) -> Tuple[Container, Settings]:
    container = Container()

    container.add_instance(settings)
    container.add_singleton(LocationQueryServiceInterface, GeolocationQueryService)

    return container, settings


class LocationQueryServiceInterface[T: LocationQueryJSON](Protocol):
    """Location aware service for listing faciltiies.
    1. Searches and fetches existing processed results by query_id for a cust_id
    2. Resolves coordinates from a given geolocation.
    3. Fetches all facilities from a given set of records for a
    given radius from geolocation.

    Radius is default for now.
    # TODO: Filter to be added
    """

    @classmethod
    @abc.abstractmethod
    async def resolve_coordinates(
        cls, reverse_geo_lookup_svc: Callable[[T], dict], query: T
    ) -> Address:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    async def fetch_facilities(
        cls,
        reverse_geo_lookup_svc: Callable[[T], dict],
        patient_query_lookup_svc: Callable[[Address, T], List[FacilitiesResult]],
        query: T,
    ) -> List[FacilitiesResult] | None:
        raise NotImplementedError


# TODO: make hard-coded response functional
class GeolocationQueryService(
    LocationQueryServiceInterface, InterfaceProtocolCheckMixin
):
    @classmethod
    async def resolve_coordinates(
        cls,
        reverse_geo_lookup_svc: Callable[[LocationQueryJSON], dict],
        query: LocationQueryJSON,
    ) -> Address:
        """Resolves to address by geo reverse lookup."""
        return Address(**reverse_geo_lookup_svc(query))

    @classmethod
    async def fetch_facilities(
        cls,
        reverse_geo_lookup_svc: Callable[[LocationQueryJSON], dict],
        patient_query_lookup_svc: Callable[
            [Address, LocationQueryJSON], List[FacilitiesResult]
        ],
        query: LocationQueryJSON,
    ) -> List[FacilitiesResult] | None:
        """Fetches facilities for a query location for a query id for a customer."""
        patient_address = await cls.resolve_coordinates(reverse_geo_lookup_svc, query)
        return patient_query_lookup_svc(patient_address, query) or None
