import pytest
import unittest

from xcov19.app.services import LocationQueryServiceInterface
from xcov19.app.dto import Address, LocationQueryJSON


@pytest.mark.usefixtures("dummy_geolocation", "stub_location_srvc")
class GeoLocationServiceTest(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def autouse(
        self,
        dummy_geolocation: LocationQueryJSON,
        stub_location_srvc: LocationQueryServiceInterface,
    ):
        self.dummy_geolocation = dummy_geolocation
        self.stub_location_srvc = stub_location_srvc

    async def test_resolve_coordinates(self):
        result = await self.stub_location_srvc.resolve_coordinates(self.dummy_geolocation)
        self.assertEqual(Address(), result)
