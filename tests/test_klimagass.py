import unittest
import pandas as pd
import sys, os
from io import StringIO

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import rensing

class TestKlimagassRens(unittest.TestCase):

    def test_klimagass_rens(self):
        data = {
            'kilde (aktivitet)': ['Olje- og gassutvinning'],
            'komponent': ['Klimagasser i alt'],
            'år': [1990]
        }
        df = pd.DataFrame(data)
        renset = rensing.klimagass_rens(df)
        self.assertEqual(len(renset), 1)
        
    #Negativ test (mangler komponent, skal da feile)
    def test_mangler_kolonne(self):
        data = {
            '"år"': [2020, 2020],
            '"verdi"': [100.0, 100.0]
        }
        df = pd.DataFrame(data)
        with self.assertRaises(KeyError):
            rensing.klimagass_rens(df)

    #Positiv test for å lese CSV-data riktig
    def test_last_in_csv(self):
        csv_str = 'år,komponent,verdi\n2020,CO2,100\n2021,CH4,80'
        csv_data = StringIO(csv_str)
        df = rensing.last_in_csv(csv_data)
        self.assertEqual(df.shape, (2, 3))
        self.assertEqual(df['verdi'].iloc[1], 80)

if __name__ == '__main__':
    unittest.main()