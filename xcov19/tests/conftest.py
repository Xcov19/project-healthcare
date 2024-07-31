import asyncio

import pytest

from xcov19.app.dto import AnonymousId, GeoLocation, LocationQueryJSON, QueryId, Address
from xcov19.app.services import LocationQueryServiceInterface

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


class StubLocationQueryServiceImpl(LocationQueryServiceInterface):
    
    @classmethod
    async def resolve_coordinates(cls, query: LocationQueryJSON) -> Address:
        yield Address()
