from typing import List
import pytest
import unittest
from xcov19.domain.models.provider import (
    Contact,
    FacilityEstablishment,
    FacilityOwnership,
    Provider,
)
from xcov19.domain.repository_interface import IProviderRepository

from xcov19.services.geolocation import (
    LocationQueryServiceInterface,
    GeolocationQueryService,
)
from xcov19.dto import Address, LocationQueryJSON, FacilitiesResult, GeoLocation


from xcov19.utils.mixins import InterfaceProtocolCheckMixin

import random

RANDOM_SEED = random.seed(1)


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
            rank=random.randint(1, 20),
            estimated_time=20,
        )
    ]


class DummyProviderRepo(IProviderRepository[Provider], InterfaceProtocolCheckMixin):
    def fetch_by_providers(self, **address: dict[str, str]) -> List[Provider]:
        return [
            Provider(
                name="Dummy Hospital",
                address="123 Test Street",
                geo_location=(0.0, 0.0),
                contact=Contact("+1234567890"),
                facility_type=FacilityEstablishment.HOSPITAL,
                ownership=FacilityOwnership.PRIVATE,
                specialties=["General", "Surgery"],
                stars=4,
                reviews=100,
            )
        ]

    def fetch_by_query(
        self, query_id: str, filtered_providers: List[Provider]
    ) -> List[Provider]:
        return [
            Provider(
                name="Dummy Hospital",
                address="123 Test Street",
                geo_location=(0.0, 0.0),
                contact=Contact("+1234567890"),
                facility_type=FacilityEstablishment.HOSPITAL,
                ownership=FacilityOwnership.PRIVATE,
                specialties=["General", "Surgery"],
                stars=4,
                reviews=100,
            )
        ]


def stub_get_facilities_by_patient_query(
    patient_address: Address,
    query: LocationQueryJSON,
    repo: IProviderRepository = DummyProviderRepo(),
) -> List[FacilitiesResult]:
    facilities_result = []
    providers = repo.fetch_by_providers(**patient_address.model_dump(round_trip=True))
    filtered_providers = repo.fetch_by_query(query.query_id.query_id, providers)
    for provider in filtered_providers:
        address_name, address1, address2 = provider.address.split()
        address = Address(name=address_name, street=f"{address1} {address2}")
        geolocation = GeoLocation(
            lat=provider.geo_location[0], lng=provider.geo_location[1]
        )

        facilities_result += [
            FacilitiesResult(
                name=provider.name,
                address=address,
                geolocation=geolocation,
                contact=provider.contact.value,
                facility_type=provider.facility_type.value,
                ownership=provider.ownership.value,
                specialties=provider.specialties,
                stars=provider.stars,
                reviews=provider.reviews,
                rank=random.randint(1, 20),
                estimated_time=20,
            )
        ]
    return facilities_result


@pytest.mark.usefixtures("dummy_geolocation_query_json", "stub_location_srvc")
class GeoLocationServiceInterfaceTest(unittest.IsolatedAsyncioTestCase):
    @pytest.fixture(autouse=True)
    def autouse(
        self,
        dummy_geolocation_query_json: LocationQueryJSON,
        stub_location_srvc: LocationQueryServiceInterface,
    ):
        self.dummy_geolocation_query_json = dummy_geolocation_query_json
        self.stub_location_srvc = stub_location_srvc

    async def test_resolve_coordinates(self):
        result = await self.stub_location_srvc.resolve_coordinates(
            dummy_reverse_geo_lookup_svc, self.dummy_geolocation_query_json
        )
        self.assertEqual(Address(), result)

    async def test_fetch_facilities(self):
        result = await self.stub_location_srvc.fetch_facilities(
            dummy_reverse_geo_lookup_svc,
            self.dummy_geolocation_query_json,
            dummy_patient_query_lookup_svc,
        )
        self.assertIsInstance(result, list)
        assert result
        self.assertTrue(
            all(isinstance(provider, FacilitiesResult) for provider in result)
        )


@pytest.mark.usefixtures("dummy_geolocation_query_json")
class GeoLocationServiceTest(unittest.IsolatedAsyncioTestCase):
    @pytest.fixture(autouse=True)
    def autouse(self, dummy_geolocation_query_json: LocationQueryJSON):
        self.dummy_geolocation_query_json = dummy_geolocation_query_json

    async def test_resolve_coordinates(self):
        result = await GeolocationQueryService.resolve_coordinates(
            dummy_reverse_geo_lookup_svc, self.dummy_geolocation_query_json
        )
        expected = Address()
        self.assertEqual(expected, result, f"Got {result}, expected {expected}")

    async def test_fetch_facilities(self):
        result = await GeolocationQueryService.fetch_facilities(
            dummy_reverse_geo_lookup_svc,
            self.dummy_geolocation_query_json,
            dummy_patient_query_lookup_svc,
        )
        self.assertIsNotNone(result)
        record = None
        if result:
            record = result[0]
        self.assertIsInstance(record, FacilitiesResult)

    async def test_fetch_facilities_no_results(self):
        result = await GeolocationQueryService.fetch_facilities(
            dummy_reverse_geo_lookup_svc,
            self.dummy_geolocation_query_json,
            dummy_patient_query_lookup_svc_none,
        )
        self.assertIsNone(result)


# @pytest.mark.skip("WIP")
@pytest.mark.usefixtures("dummy_geolocation_query_json")
class PatientQueryLookupSvcTest(unittest.IsolatedAsyncioTestCase):
    @pytest.fixture(autouse=True)
    def autouse(self, dummy_geolocation_query_json: LocationQueryJSON):
        self.dummy_geolocation_query_json = dummy_geolocation_query_json

    async def test_patient_query_lookup_svc(self):
        providers = await GeolocationQueryService.fetch_facilities(
            dummy_reverse_geo_lookup_svc,
            self.dummy_geolocation_query_json,
            stub_get_facilities_by_patient_query,
        )
        self.assertIsInstance(providers, list)
        assert providers
        self.assertTrue(
            all(isinstance(provider, FacilitiesResult) for provider in providers)
        )
