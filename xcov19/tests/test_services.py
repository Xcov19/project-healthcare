import pytest
import unittest

from xcov19.app.services import LocationQueryServiceInterface
from xcov19.app.dto import Address, LocationQueryJSON, FacilitiesResult, GeoLocation


@pytest.mark.usefixtures("dummy_geolocation", "stub_location_srvc")
class GeoLocationServiceTest(unittest.IsolatedAsyncioTestCase):
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
            self.dummy_geolocation
        )
        self.assertEqual(Address(), result)

    async def test_fetch_facilities(self):
        result = await self.stub_location_srvc.fetch_facilities(self.dummy_geolocation)
        expected = FacilitiesResult(
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
        self.assertEqual(expected, result)
