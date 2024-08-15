import pytest
import unittest

from xcov19.app.services import LocationQueryServiceInterface, GeolocationQueryService
from xcov19.app.dto import Address, LocationQueryJSON, FacilitiesResult, GeoLocation


def dummy_reverse_geo_lookup_svc(query: LocationQueryJSON) -> dict:
    return {}


def dummy_patient_query_lookup_svc_none(
    address: Address, query: LocationQueryJSON
) -> list:
    return []


def dummy_patient_query_lookup_svc(address: Address, query: LocationQueryJSON) -> list:
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


@pytest.mark.usefixtures("dummy_geolocation", "stub_location_srvc")
class GeoLocationServiceInterfaceTest(unittest.IsolatedAsyncioTestCase):
    @pytest.fixture(autouse=True)
    def autouse(
        self,
        dummy_geolocation: LocationQueryJSON,
        stub_location_srvc: LocationQueryServiceInterface,
    ):
        self.dummy_geolocation = dummy_geolocation
        self.stub_location_srvc = stub_location_srvc

    async def test_resolve_coordinates(self):
        result = await self.stub_location_srvc.resolve_coordinates(
            dummy_reverse_geo_lookup_svc, self.dummy_geolocation
        )
        self.assertEqual(Address(), result)

    async def test_fetch_facilities(self):
        result = await self.stub_location_srvc.fetch_facilities(
            dummy_reverse_geo_lookup_svc,
            dummy_patient_query_lookup_svc,
            self.dummy_geolocation,
        )
        self.assertIsInstance(result, list)


@pytest.mark.usefixtures("dummy_geolocation", "stub_location_srvc")
class GeoLocationServiceTest(unittest.IsolatedAsyncioTestCase):
    @pytest.fixture(autouse=True)
    def autouse(self, dummy_geolocation: LocationQueryJSON):
        self.dummy_geolocation = dummy_geolocation

    async def test_resolve_coordinates(self):
        result = await GeolocationQueryService.resolve_coordinates(
            dummy_reverse_geo_lookup_svc, self.dummy_geolocation
        )
        expected = Address()
        self.assertEqual(expected, result, f"Got {result}, expected {expected}")

    async def test_fetch_facilities(self):
        result = await GeolocationQueryService.fetch_facilities(
            dummy_reverse_geo_lookup_svc,
            dummy_patient_query_lookup_svc,
            self.dummy_geolocation,
        )
        self.assertIsNotNone(result)
        record = None
        if result:
            record = result[0]
        self.assertIsInstance(record, FacilitiesResult)

    async def test_fetch_facilities_no_results(self):
        result = await GeolocationQueryService.fetch_facilities(
            dummy_reverse_geo_lookup_svc,
            dummy_patient_query_lookup_svc_none,
            self.dummy_geolocation,
        )
        self.assertIsNone(result)
