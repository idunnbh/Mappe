import unittest
import os
import json
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from dotenv import load_dotenv
load_dotenv()

from datainnsamling_luftkvalitet import fetch_air_quality_data


class TestFetchAirQualityData(unittest.TestCase):
    def setUp(self):
        #Setter opp konstanter for testene, som API-URL, params og headers
        self.api_url = "https://api.met.no/weatherapi/airqualityforecast/0.1/"
        self.params = {"lat": "63.4195", "lon": "10.4065"}
        self.headers = {
            "User-Agent": os.getenv("IDUNN_USER_AGENT", "DefaultUserAgent/1.0")
        }
    
    def test_fetch_success(self):
        #Tester at funksjonen returnerer en dict når forespørselen lykkes
        data = fetch_air_quality_data(self.api_url, self.params, self.headers)
        self.assertIsInstance(data, dict)

    def test_fetch_failure(self):
        #Tester at funksjonen kaster en Exception hvis URL-en er feil
        with self.assertRaises(Exception):
            fetch_air_quality_data("https://api.met.no/feilurl", self.params, self.headers)

if __name__ == '__main__':
    unittest.main()
