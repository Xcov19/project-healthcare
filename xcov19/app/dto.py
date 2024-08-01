from blacksheep import FromHeader
from pydantic import BaseModel, Field

from typing import Annotated, List


class FromOriginMatchHeader(FromHeader[str]):
    name = "X-Origin-Match-Header"
    secret = "secret"


class GeoLocation(BaseModel):
    lat: float
    lng: float


class Address(BaseModel):
    name: str | None = Field(default=None)
    street: str | None = Field(default=None)
    city: str | None = Field(default=None)
    state: str | None = Field(default=None)
    zip: str | None = Field(default=None)
    country: str | None = Field(default=None)


class AnonymousId(BaseModel):
    cust_id: str


class QueryId(BaseModel):
    query_id: str


class LocationQueryJSON(BaseModel):
    location: GeoLocation
    cust_id: AnonymousId
    query_id: QueryId


class DiagnosisQueryJSON(BaseModel):
    query: str
    query_id: QueryId


class FacilitiesResult(BaseModel):
    name: str
    address: Address
    geolocation: GeoLocation
    contact: str
    facility_type: Annotated[str, Field(...)]
    ownership: Annotated[str, Field(...)]
    specialties: Annotated[List[str], Field(...)]
    stars: Annotated[int, Field(ge=1, le=5)]
    reviews: Annotated[int, Field(ge=0)]
    rank: Annotated[int, Field(default=1, gt=0, le=20)]
    estimated_time: Annotated[float, Field(default=0.0, ge=0)]
