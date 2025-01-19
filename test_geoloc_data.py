import os
import pytest
from geoloc_util import verify_api_key, fetch_location_data

# Mock valid API key and input data for testing
VALID_API_KEY = "test_api_key"
os.environ["OPENWEATHER_API_KEY"] = VALID_API_KEY

# Mock response data for testing
mock_response_single = {
    "lat": 43.0731,
    "lon": -89.4012,
    "name": "Madison",
    "state": "Wisconsin",
    "country": "United States",
}

mock_response_multiple = [
    {"lat": 41.8781, "lon": -87.6298, "name": "Chicago", "state": "Illinois", "country": "United States"},
    {"lat": 40.7128, "lon": -74.0060, "name": "New York", "state": "New York", "country": "United States"},
]

@pytest.fixture
def mock_fetch_location_data(monkeypatch):
    def mock_function(location):
        if location == "Madison, WI":
            return mock_response_single
        elif location == "Chicago, IL":
            return mock_response_multiple[0]
        elif location == "New York, NY":
            return mock_response_multiple[1]
        else:
            raise ValueError("Invalid location input")
    monkeypatch.setattr("geoloc_util.fetch_location_data", mock_function)

def test_verify_api_key_exists():
    """Test if verify_api_key raises an exception for missing API key."""
    del os.environ["OPENWEATHER_API_KEY"]  # Temporarily remove the API key
    with pytest.raises(EnvironmentError, match="API key not found"):
        verify_api_key()
    os.environ["OPENWEATHER_API_KEY"] = VALID_API_KEY  # Restore API key

def test_fetch_single_location(mock_fetch_location_data):
    """Test fetching data for a single location."""
    result = fetch_location_data("Madison, WI")
    assert result["lat"] == 43.0731
    assert result["lon"] == -89.4012
    assert result["name"] == "Madison"

def test_fetch_multiple_locations(mock_fetch_location_data):
    """Test fetching data for multiple locations."""
    locations = ["Chicago, IL", "New York, NY"]
    results = [fetch_location_data(location) for location in locations]

    assert len(results) == 2

    assert results[0]["name"] == "Chicago"
    assert results[0]["lat"] == 41.8781
    assert results[0]["lon"] == -87.6298

    assert results[1]["name"] == "New York"
    assert results[1]["lat"] == 40.7128
    assert results[1]["lon"] == -74.0060
