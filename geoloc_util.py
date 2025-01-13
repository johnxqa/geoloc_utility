import argparse
import os
import requests

API_BASE_URL = "http://api.openweathermap.org/geo/1.0"
COUNTRY_CODE = "US"

def get_api_key():
    """
    Verifies that the 'API_KEY' environment variable exists and has a value.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise EnvironmentError("The 'API_KEY' environment variable is not set or is empty.")
    return api_key

def fetch_location_info(location):
    """Fetches location information for a given city/state or zip code."""
    API_KEY = get_api_key()
    if "," in location:  # City, State format
        endpoint = f"{API_BASE_URL}/direct"
        params = {"q": f"{location},{COUNTRY_CODE}", "limit": 1, "appid": API_KEY}
    else:  # Zip code format
        endpoint = f"{API_BASE_URL}/zip"
        params = {"zip": f"{location},{COUNTRY_CODE}", "appid": API_KEY}
    
    response = requests.get(endpoint, params=params)
    if response.status_code != 200:
        raise ValueError(f"API Error: {response.status_code} - {response.text}")
    
    data = response.json()
    if not data:
        return f"No results found for {location}"
    
    # Extract necessary information
    if isinstance(data, list):  # City, State result
        result = data[0]
    else:  # Zip code result
        result = data

    return {
        "latitude": result.get("lat"),
        "longitude": result.get("lon"),
        "place_name": result.get("name", result.get("zip")),
        "country": result.get("country")
    }


def main():
    parser = argparse.ArgumentParser(description="Geolocation Utility")
    parser.add_argument(
        "locations", nargs="+", help="List of locations in 'City, State' or 'Zip Code' format."
    )
    args = parser.parse_args()

    for location in args.locations:
        try:
            result = fetch_location_info(location)
            print(f"{location}: {result}")
        except Exception as e:
            print(f"Error processing {location}: {e}")


if __name__ == "__main__":
    main()
