import os
import unittest
from geoloc_util import fetch_location_info, get_api_key


class TestGeolocUtil(unittest.TestCase):
    def test_valid_city_state(self):
        result = fetch_location_info("Madison, WI")
        self.assertIn("latitude", result)
        self.assertIn("longitude", result)
    
    def test_valid_zip_code(self):
        result = fetch_location_info("12345")
        self.assertIn("latitude", result)
        self.assertIn("longitude", result)
    
    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            fetch_location_info("InvalidInput")
    
    def test_no_results(self):
        result = fetch_location_info("FakeCity, ZZ")
        self.assertEqual(result, "No results found for FakeCity, ZZ")

    def test_missing_api_key(self):
        with self.assertRaises(OSError):
            current_key = os.getenv("OPENWEATHER_API_KEY")
            os.environ["OPENWEATHER_API_KEY"] = ""
            get_api_key()
        os.environ["OPENWEATHER_API_KEY"] = current_key



if __name__ == "__main__":
    unittest.main()
