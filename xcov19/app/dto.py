from blacksheep import FromHeader
from pydantic import BaseModel, Field


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
