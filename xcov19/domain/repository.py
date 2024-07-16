from typing import Protocol
import abc

from xcov19.domain.models.patient import Patient
from xcov19.domain.models.provider import Provider


class IPatientStore[T: Patient](Protocol):
    @classmethod
    @abc.abstractmethod
    def enqueue_diagnosis_query(cls, patient: T):
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def enqueue_geolocation_query(cls, patient: T):
        raise NotImplementedError


class IProviderStore[T: Provider](Protocol):
    @classmethod
    @abc.abstractmethod
    def fetch(cls, provider: T):
        raise NotImplementedError
