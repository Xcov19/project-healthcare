from typing import Protocol, TypeVar, List
import abc

from xcov19.domain.models.patient import Patient
from xcov19.domain.models.provider import Provider

PatientT = TypeVar("PatientT", bound=Patient)
ProviderT = TypeVar("ProviderT", bound=Patient)


class IPatientStore[PatientT: Patient](Protocol):
    @classmethod
    @abc.abstractmethod
    def enqueue_diagnosis_query(cls, patient: PatientT):
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def enqueue_geolocation_query(cls, patient: PatientT):
        raise NotImplementedError


class IProviderRepository[ProviderT: Provider](Protocol):
    @abc.abstractmethod
    def fetch_by_providers(self, **address: dict[str, str]) -> List[ProviderT]:
        raise NotImplementedError

    @abc.abstractmethod
    def fetch_by_query(
        self, query_id: str, filtered_providers: List[ProviderT]
    ) -> List[ProviderT]:
        raise NotImplementedError
