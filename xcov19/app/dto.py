from blacksheep import FromHeader
from pydantic import BaseModel


class FromOriginMatchHeader(FromHeader[str]):
    name = "X-Origin-Match-Header"
    secret = "secret"


class GeoLocation(BaseModel):
    lat: float
    lng: float


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
