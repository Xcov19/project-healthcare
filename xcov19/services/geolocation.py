from __future__ import annotations

import abc
from typing import TypeVar, Protocol, Callable, List

from xcov19.dto import LocationQueryJSON, Address, FacilitiesResult
from xcov19.utils.mixins import InterfaceProtocolCheckMixin

T = TypeVar("T", bound=LocationQueryJSON)


# Application services


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
        query: T,
        patient_query_lookup_svc: Callable[[Address, T], List[FacilitiesResult]],
    ) -> List[FacilitiesResult] | None:
        raise NotImplementedError


class GeolocationQueryService(
    LocationQueryServiceInterface[LocationQueryJSON], InterfaceProtocolCheckMixin
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
        query: LocationQueryJSON,
        patient_query_lookup_svc: Callable[
            [Address, LocationQueryJSON],
            List[FacilitiesResult],
        ],
    ) -> List[FacilitiesResult] | None:
        """Fetches facilities for a query location for a query id for a customer."""
        patient_address = await cls.resolve_coordinates(reverse_geo_lookup_svc, query)
        return patient_query_lookup_svc(patient_address, query) or None
