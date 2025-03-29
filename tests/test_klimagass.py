import unittest
import pandas as pd
import sys, os
from io import StringIO

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import rensing

class TestKlimagass(unittest.TestCase):
#Positiv test for rensing av kolonnenavn
    def test_rense_kolonnenavn(self):
        data = {
            '"år"': [],
            '"komponent"': [],
            '"verdi"': []
        }
        df = pd.DataFrame(data)
        df_renset = rensing.rense_kolonnenavn(df)
        self.assertListEqual(list(df_renset.columns), ['år', 'komponent', 'verdi'])

#Positiv test for å lese CSV-data riktig
    def test_last_in_csv(self):
        csv_str = 'år,komponent,verdi\n2020,CO2,100\n2021,CH4,80'
        csv_data = StringIO(csv_str)
        df = rensing.last_in_csv(csv_data)
        self.assertEqual(df.shape, (2, 3))
        self.assertEqual(df['verdi'].iloc[1], 80)

#Negativ test (mangler komponent, skal da feile)
    def test_mangler_kolonne(self):
        data = {
            '"år"': [2020, 2020],
            '"verdi"': [100.0, 100.0]
        }
        df = pd.DataFrame(data)
        with self.assertRaises(KeyError):
            rensing.klimagass_rens(df)

if __name__ == '__main__':
    unittest.main()