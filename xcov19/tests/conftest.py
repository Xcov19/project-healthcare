from collections.abc import Callable

import pytest

from xcov19.app.dto import (
    AnonymousId,
    GeoLocation,
    LocationQueryJSON,
    QueryId,
    Address,
    FacilitiesResult,
)
from xcov19.app.services import LocationQueryServiceInterface
from xcov19.utils.mixins import InterfaceProtocolCheckMixin

# Same as using @pytest.mark.anyio
pytestmark = pytest.mark.anyio


# Change the backend option for all project
@pytest.fixture(
    params=[
        pytest.param(("asyncio", {"use_uvloop": True}), id="asyncio+uvloop"),
    ]
)
def anyio_backend(request):
    return request.param


@pytest.fixture(scope="class")
def dummy_coordinates():
    return GeoLocation(lat=0, lng=0)


@pytest.fixture(scope="class")
def dummy_geolocation(dummy_coordinates):
    return LocationQueryJSON(
        location=dummy_coordinates,
        cust_id=AnonymousId(cust_id="test_cust_id"),
        query_id=QueryId(query_id="test_query_id"),
    )


@pytest.fixture(scope="class")
def stub_location_srvc():
    return StubLocationQueryServiceImpl


class StubLocationQueryServiceImpl(
    LocationQueryServiceInterface, InterfaceProtocolCheckMixin
):
    @classmethod
    async def resolve_coordinates(
        cls,
        reverse_geo_lookup_svc: Callable[[LocationQueryJSON], dict],
        query: LocationQueryJSON,
    ) -> Address:
        return Address(**reverse_geo_lookup_svc(query))

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
