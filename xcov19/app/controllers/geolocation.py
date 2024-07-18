"""Controller API routes for geolocation."""

from blacksheep import Response, FromJSON, ok
from blacksheep.server.controllers import APIController, post

from xcov19.app.dto import LocationQueryJSON, FromOriginMatchHeader


class GeolocationController(APIController):
    @classmethod
    def route(cls) -> str | None:
        return "api/geo"

    @classmethod
    def version(cls) -> str:
        return "v1"

    @post()
    async def location_query(
        self,
        location_query: FromJSON[LocationQueryJSON],
        _from_origin_header: FromOriginMatchHeader,
    ) -> Response:
        # TODO: Implement Geolocation application service GeoLocationService
        # Service should Enqueue request, filter matching rows by geolocation,
        #   store in a temp row in aux sheet/table.
        # dummy impl
        print(location_query.value)
        return ok()
