from collections.abc import Callable
from typing import List

from blacksheep.testing import TestClient
import pytest

from blacksheep import Application
from xcov19.dto import (
    AnonymousId,
    GeoLocation,
    LocationQueryJSON,
    QueryId,
    Address,
    FacilitiesResult,
)
from xcov19.services.geolocation import LocationQueryServiceInterface
from xcov19.utils.mixins import InterfaceProtocolCheckMixin

import random

RANDOM_SEED = random.seed(1)

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
def dummy_coordinates() -> GeoLocation:
    return GeoLocation(lat=0, lng=0)


@pytest.fixture(scope="class")
def dummy_geolocation_query_json(dummy_coordinates) -> LocationQueryJSON:
    return LocationQueryJSON(
        location=dummy_coordinates,
        cust_id=AnonymousId(cust_id="test_cust_id"),
        query_id=QueryId(query_id="test_query_id"),
    )


@pytest.fixture(scope="class")
def dummy_reverse_geo_lookup_svc() -> Callable[[LocationQueryJSON], dict]:
    def callback(query: LocationQueryJSON) -> dict:
        return {}

    return callback


@pytest.fixture(scope="class")
def dummy_patient_query_lookup_svc_none() -> (
    Callable[[Address, LocationQueryJSON], list]
):
    def callback(address: Address, query: LocationQueryJSON) -> list:
        return []

    return callback


@pytest.fixture(scope="class")
def dummy_patient_query_lookup_svc() -> Callable[[Address, LocationQueryJSON], list]:
    def callback(address: Address, query: LocationQueryJSON) -> list:
        return [
            FacilitiesResult(
                name="Test facility",
                address=Address(),
                geolocation=GeoLocation(lat=0.0, lng=0.0),
                contact="+919999999999",
                facility_type="nursing",
                ownership="charity",
                specialties=["surgery", "pediatrics"],
                stars=4,
                reviews=120,
                rank=random.randint(1, 20),
                estimated_time=20,
            )
        ]

    return callback


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
    async def fetch_facilities(
        cls,
        reverse_geo_lookup_svc: Callable[[LocationQueryJSON], dict],
        query: LocationQueryJSON,
        patient_query_lookup_svc: Callable[
            [Address, LocationQueryJSON], List[FacilitiesResult]
        ],
    ) -> List[FacilitiesResult] | None:
        return [
            FacilitiesResult(
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
        ]


@pytest.fixture(scope="class")
def stub_location_srvc() -> LocationQueryServiceInterface:
    return StubLocationQueryServiceImpl


@pytest.fixture(scope="function", name="client")
async def test_client():
    # Create a test client
    async def start_client(app: Application) -> TestClient:
        return TestClient(app)

    return start_client
