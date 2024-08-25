"""Controller API routes for geolocation."""

from blacksheep import Response, ok, FromJSON
from blacksheep.server.controllers import APIController

from xcov19.app.controllers import post
from xcov19.dto import LocationQueryJSON
from xcov19.app.settings import FromOriginMatchHeader

from xcov19.services.geolocation import LocationQueryServiceInterface


class GeolocationController(APIController):
    @classmethod
    def route(cls) -> str | None:
        return "geo"

    @classmethod
    def version(cls) -> str:
        return "v1"

    @post()
    async def location_query(
        self,
        location_query: FromJSON[LocationQueryJSON],
        geo_service: LocationQueryServiceInterface,
        _from_origin_header: FromOriginMatchHeader,
    ) -> Response:
        # TODO: Implement Geolocation application service GeoLocationService
        # Service should Enqueue request, filter matching rows by geolocation,
        #   store in a temp row in aux sheet/table.
        # dummy impl
        print(location_query.value)
        return ok()
