import dataclasses
import enum
from dataclasses import dataclass
from typing import Annotated, List
from xcov19.domain.models import MobileTelephone, GeoLocation


# values
class FacilityEstablishment(enum.StrEnum):
    HOSPITAL = "hospital"
    CLINIC = "clinic"
    NURSING = "nursing"
    LAB = "lab"
    PHARMACY = "pharmacy"


class FacilityOwnership(enum.StrEnum):
    GOVERNMENT = "government"
    PRIVATE = "private"
    PUBLIC = "public"
    PUB_PVT = "public-private"
    CHARITY = "charity"


type FacilityType = FacilityEstablishment
type FacilityOwnerType = FacilityOwnership
type ProviderName = str
type Specialties = List[str]
type Qualification = List[str]
type PracticeExpYears = int | float
type MoneyType = int | float


@dataclass
class Contact[T: MobileTelephone]:
    value: T

    def _valid_prefix(self) -> bool:
        return self.value[0] == "+" or ord("0") <= ord(self.value[0]) <= ord("9")

    def __post_init__(self):
        if not self._valid_prefix() and any(
            not each.isdigit() for each in self.value[1:]
        ):
            raise ValueError("Invalid phone number format.")


@dataclass
class Stars:
    value: int | float = dataclasses.field(default=1)
    min_rating: dataclasses.InitVar[int] = dataclasses.field(default=1)
    max_rating: dataclasses.InitVar[int] = dataclasses.field(default=5)

    def __post_init__(self, min_rating, max_rating):
        if not min_rating <= self.value <= max_rating:
            raise ValueError(f"Rating must be between {min_rating} and {max_rating}.")


@dataclass
class Reviews:
    value: int = dataclasses.field(default=0, init=True)

    def __post_init__(self):
        if self.value < 0:
            raise ValueError("Reviews cannot be negative.")


# domain entities


@dataclass
class Doctor:
    name: str
    specialties: Specialties
    degree: Qualification
    experience: PracticeExpYears
    fee: MoneyType


@dataclass
class Provider:
    name: ProviderName
    address: str
    geo_location: GeoLocation
    contact: Contact
    facility_type: FacilityType
    ownership: FacilityOwnerType
    specialties: Specialties
    available_doctors: List[Doctor]
    stars: Annotated[int, Stars(min_rating=1, max_rating=5)]
    reviews: Annotated[int, Reviews(value=0)]
