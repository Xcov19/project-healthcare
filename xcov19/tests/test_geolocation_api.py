import json
import pytest
from xcov19.dto import LocationQueryJSON, GeoLocation, AnonymousId, QueryId
from blacksheep import Content, Response


@pytest.mark.api
@pytest.mark.usefixtures("client")
class TestGeolocationAPI:
    async def test_location_query_endpoint(self, client):
        # Prepare the request payload
        location_query = LocationQueryJSON(
            location=GeoLocation(lat=0, lng=0),
            cust_id=AnonymousId(cust_id="test_cust_id"),
            query_id=QueryId(query_id="test_query_id"),
        )

        # Send a POST request to the /geo endpoint
        query = location_query.model_dump(round_trip=True)
        binary_data = json.dumps(query).encode("utf-8")
        print("binary data", binary_data, type(binary_data))
        response: Response = await client.post(
            "/geo",
            content=Content(b"application/json", binary_data),
            # Add the required header
            headers={
                "X-Origin-Match-Header": "secret",
            },
        )

        # The current implementation returns ok(), which is null in JSON
        # response_text = await response.text()
        # assert response_text.lower() == "resource not found"
        # Assert the response
        assert response.content_type() == b"text/plain; charset=utf-8"
        # assert response.content == b''
        assert response.status == 200
