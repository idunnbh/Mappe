import os
import sys
import unittest

import pandas as pd
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

load_dotenv()

from datainnsamling_temperatur import hent_sanntidsdata, hent_temperaturer, hent_historiske_temperaturer
import rensing 

class TestTemperaturHenting(unittest.TestCase):
    def setUp(self):
        self.lat = 63.4195
        self.lon = 10.4065

    def test_hent_sanntidsdata_returnerer_dict(self):
        "Sanntidsdata skal returnere en ordbok med 'properties'-nøkkel."
        data = hent_sanntidsdata(self.lat, self.lon)
        self.assertIsInstance(data, dict)
        self.assertIn("properties", data)

    def test_hent_sanntidsdata_feiler_uten_user_agent(self):
        "Skal kaste ValueError hvis USER_AGENT mangler."
        original = os.environ.get("USER_AGENT")
        os.environ["USER_AGENT"] = ""

        with self.assertRaises(ValueError):
            hent_sanntidsdata(self.lat, self.lon)

        if original:
            os.environ["USER_AGENT"] = original

    def test_hent_sanntidsdata_inneholder_temperatur(self):
        data = hent_sanntidsdata(self.lat, self.lon)
        temps = hent_temperaturer(data)
        self.assertTrue(len(temps) > 0)
        self.assertIsInstance(temps[0], tuple)
        self.assertIsInstance(temps[0][1], float)


    def test_hent_historiske_temperaturer_feiler_uten_api_nokkel(self):
        "Skal kaste ValueError hvis FROST_API_KEY mangler."
        original = os.environ.get("FROST_API_KEY")
        os.environ["FROST_API_KEY"] = ""

        with self.assertRaises(ValueError):
            hent_historiske_temperaturer()

        if original:
            os.environ["FROST_API_KEY"] = original


# Testklasse for hent_temperaturer
class TestTemperaturParsing(unittest.TestCase):
    def test_hent_temperaturer_returnerer_liste(self):
        "Funksjonen skal returnere en liste med tidspunkt, temperatur"
        dummy_data = {
            "properties": {
                "timeseries": [
                    {
                        "time": "2025-01-01T00:00:00Z",
                        "data": {
                            "instant": {
                                "details": {
                                    "air_temperature": 15
                                }
                            }
                        }
                    }
                ]
            }
        }

        resultat = hent_temperaturer(dummy_data)
        self.assertIsInstance(resultat, list)
        self.assertEqual(resultat[0][1], 15)

# Testklasse for temperatur_rens
class TestTemperaturRensing(unittest.TestCase):
    def test_temperatur_rens(self):
        "Skal håndtere manglende verdier, outliers og duplikater."
        data = {
            'tidspunkt': ['2025-01-01 12:00', '2025-01-01 12:00'],
            'temperatur': [None, 15]  
        }
        df = pd.DataFrame(data)
        df_renset = rensing.temperatur_rens(df)
        self.assertEqual(len(df_renset), 1)


# Test suite som kjører klassene
def test_suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestTemperaturHenting))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestTemperaturParsing))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestTemperaturRensing))
    return suite

if __name__ == "__main__":
    unittest.main()