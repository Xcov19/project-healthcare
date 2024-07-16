from dataclasses import dataclass

from xcov19.domain.models import GeoLocation

type CustomerId = str

# domain entities


@dataclass
class Patient:
    cust_id: CustomerId
    query: str
    geo_location: GeoLocation
