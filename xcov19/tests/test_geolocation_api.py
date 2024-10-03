import json
import pytest
from xcov19.dto import LocationQueryJSON, GeoLocation, AnonymousId, QueryId
from blacksheep import Content, Response


@pytest.mark.integration
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
            # Add the required Header
            headers={
                "X-Origin-Match-Header": "secret",
            },
        )

        # Check if the response status is OK (200)
        assert response.status == 200, f"Expected status 200 but got {response.status}"

        # Check if content type is as expected
        assert response.content_type() == b"text/plain; charset=utf-8", f"Unexpected content type: {response.content_type()}"

        # Validate response body (assuming it should return a JSON object)
        try:
            response_data = await response.json()
            assert "expected_key" in response_data, "Response JSON does not contain expected key"
            # Add more assertions based on expected structure of response_data
        except Exception as e:
            pytest.fail(f"Failed to parse JSON response: {e}")
