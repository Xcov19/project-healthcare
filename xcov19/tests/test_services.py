from collections.abc import Callable
from typing import List
import pytest
import unittest
import random


from xcov19.domain.models.provider import (
    Contact,
    Doctor,
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

RANDOM_SEED = random.seed(1)


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
                available_doctors=[
                    Doctor(
                        name="Dr. Smith",
                        specialties=["General"],
                        degree=["MBBS"],
                        experience=5,
                        fee=250.00,
                    )
                ],
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
                available_doctors=[
                    Doctor(
                        name="Dr. Smith",
                        specialties=["General"],
                        degree=["MBBS"],
                        experience=5,
                        fee=250.00,
                    )
                ],
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


@pytest.mark.usefixtures(
    "dummy_geolocation_query_json",
    "dummy_reverse_geo_lookup_svc",
    "dummy_patient_query_lookup_svc",
    "stub_location_srvc",
)
class GeoLocationServiceInterfaceTest(unittest.IsolatedAsyncioTestCase):
    @pytest.fixture(autouse=True)
    def autouse(
        self,
        dummy_geolocation_query_json: LocationQueryJSON,
        dummy_reverse_geo_lookup_svc: Callable[[LocationQueryJSON], dict],
        dummy_patient_query_lookup_svc: Callable[[Address, LocationQueryJSON], list],
        stub_location_srvc: LocationQueryServiceInterface,
    ):
        self.dummy_geolocation_query_json = dummy_geolocation_query_json
        self.dummy_reverse_geo_lookup_svc = dummy_reverse_geo_lookup_svc
        self.dummy_patient_query_lookup_svc = dummy_patient_query_lookup_svc
        self.stub_location_srvc = stub_location_srvc

    async def test_resolve_coordinates(self):
        result = await self.stub_location_srvc.resolve_coordinates(
            self.dummy_reverse_geo_lookup_svc, self.dummy_geolocation_query_json
        )
        self.assertEqual(Address(), result)

    async def test_fetch_facilities(self):
        result = await self.stub_location_srvc.fetch_facilities(
            self.dummy_reverse_geo_lookup_svc,
            self.dummy_geolocation_query_json,
            self.dummy_patient_query_lookup_svc,
        )
        self.assertIsInstance(result, list)
        assert result
        self.assertTrue(
            all(isinstance(provider, FacilitiesResult) for provider in result)
        )


@pytest.mark.usefixtures(
    "dummy_geolocation_query_json",
    "dummy_reverse_geo_lookup_svc",
    "dummy_patient_query_lookup_svc",
    "dummy_patient_query_lookup_svc_none",
)
class GeoLocationServiceTest(unittest.IsolatedAsyncioTestCase):
    @pytest.fixture(autouse=True)
    def autouse(
        self,
        dummy_geolocation_query_json: LocationQueryJSON,
        dummy_reverse_geo_lookup_svc: Callable[[LocationQueryJSON], dict],
        dummy_patient_query_lookup_svc: Callable[[Address, LocationQueryJSON], list],
        dummy_patient_query_lookup_svc_none: Callable[
            [Address, LocationQueryJSON], list
        ],
    ):
        self.dummy_geolocation_query_json = dummy_geolocation_query_json
        self.dummy_reverse_geo_lookup_svc = dummy_reverse_geo_lookup_svc
        self.dummy_patient_query_lookup_svc = dummy_patient_query_lookup_svc
        self.dummy_patient_query_lookup_svc_none = dummy_patient_query_lookup_svc_none

    async def test_resolve_coordinates(self):
        result = await GeolocationQueryService.resolve_coordinates(
            self.dummy_reverse_geo_lookup_svc, self.dummy_geolocation_query_json
        )
        expected = Address()
        self.assertEqual(expected, result, f"Got {result}, expected {expected}")

    async def test_fetch_facilities(self):
        result = await GeolocationQueryService.fetch_facilities(
            self.dummy_reverse_geo_lookup_svc,
            self.dummy_geolocation_query_json,
            self.dummy_patient_query_lookup_svc,
        )
        self.assertIsNotNone(result)
        record = None
        if result:
            record = result[0]
        self.assertIsInstance(record, FacilitiesResult)

    async def test_fetch_facilities_no_results(self):
        result = await GeolocationQueryService.fetch_facilities(
            self.dummy_reverse_geo_lookup_svc,
            self.dummy_geolocation_query_json,
            self.dummy_patient_query_lookup_svc_none,
        )
        self.assertIsNone(result)


# @pytest.mark.skip(reason="WIP")
# @pytest.mark.integration
# @pytest.mark.usefixtures("dummy_reverse_geo_lookup_svc", "dummy_geolocation_query_json")
# class GeoLocationServiceSqlRepoDBTest(unittest.IsolatedAsyncioTestCase):
# """Test case for Sqlite Repository to test Geolocation Service.

# Before testing, ensure to:
# 1. Setup Database
# 2. For fetch_facilities, relevant services are configured.
# 3. patient_query_lookup_svc is configured to call sqlite repository.
# """

# @pytest.fixture(autouse=True)
# def autouse(
#     self,
#     dummy_geolocation_query_json: LocationQueryJSON,
#     dummy_reverse_geo_lookup_svc: Callable[[LocationQueryJSON], dict],
# ):
#     self.dummy_geolocation_query_json = dummy_geolocation_query_json
#     self.dummy_reverse_geo_lookup_svc = dummy_reverse_geo_lookup_svc

# async def asyncSetUp(self) -> None:
#     self._test_db = SetUpTestDatabase()
#     await self._test_db.setup_test_database()
#     self._session = await self._test_db.start_async_session()
#     assert isinstance(self._session, AsyncSessionWrapper)
#     await seed_data(self._session)
#     await super().asyncSetUp()

# async def asyncTearDown(self) -> None:
#     await self._test_db.aclose()
#     await super().asyncTearDown()

# def _patient_query_lookup_svc_using_repo(
#     self, address: Address, query: LocationQueryJSON
# ) -> List[FacilitiesResult]:
#     # TODO: Implement a patient query lookup service
#     # that returns type List[FacilitiesResult]
#     repo: IProviderRepository = SqliteProviderRepo(self._session)
#     # TODO: change repo fetch_by_providers to List facilties, not providers.
#     providers: List[Provider] = repo.fetch_by_providers(
#         **address.model_dump(round_trip=True)
#     )
#     return repo.fetch_by_query(query.query_id.query_id, providers)

# async def test_fetch_facilities(self):
#     # TODO Implement test_fetch_facilities like this:
#     facilities = await GeolocationQueryService.fetch_facilities(
#         self.dummy_reverse_geo_lookup_svc,
#         self.dummy_geolocation_query_json,
#         self._patient_query_lookup_svc_using_repo,
#     )
#     assert facilities
#     self.assertIsInstance(facilities, list)
#     self.assertIs(len(facilities), 1)


@pytest.mark.usefixtures("dummy_geolocation_query_json", "dummy_reverse_geo_lookup_svc")
class PatientQueryLookupSvcTest(unittest.IsolatedAsyncioTestCase):
    @pytest.fixture(autouse=True)
    def autouse(
        self,
        dummy_geolocation_query_json: LocationQueryJSON,
        dummy_reverse_geo_lookup_svc: Callable[[LocationQueryJSON], dict],
    ):
        self.dummy_geolocation_query_json = dummy_geolocation_query_json
        self.dummy_reverse_geo_lookup_svc = dummy_reverse_geo_lookup_svc

    async def test_patient_query_lookup_svc(self):
        providers = await GeolocationQueryService.fetch_facilities(
            self.dummy_reverse_geo_lookup_svc,
            self.dummy_geolocation_query_json,
            stub_get_facilities_by_patient_query,
        )
        self.assertIsInstance(providers, list)
        assert providers
        self.assertTrue(
            all(isinstance(provider, FacilitiesResult) for provider in providers)
        )
