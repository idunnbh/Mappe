import os
import sys
import tempfile
from contextlib import redirect_stdout
from io import StringIO
import unittest

import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import rensing
import run_rensing

class TestKlimagassRens(unittest.TestCase):

    def test_klimagass_rens_norge(self):
        data = {
            'kilde (aktivitet)': ['Olje- og gassutvinning'],
            'komponent': ['Klimagasser i alt'],
            'år': [1990]
        }
        df = pd.DataFrame(data)
        renset = rensing.klimagass_rens(df)
        self.assertEqual(len(renset), 1)

    def test_klimagass_rens_verden(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Opprett midlertidig data-mappe
            data_dir = os.path.join(tmpdir, "data")
            os.makedirs(data_dir, exist_ok=True)

            # Lager testfil med innhold
            input_path = os.path.join(data_dir, "klimagassutslipp_verden.csv")
            output_path = os.path.join(data_dir, "klimagassutslipp_verden_renset.csv")

            with open(input_path, "w", encoding="utf-8") as f:
                f.write("Year,Annual greenhouse gas emissions in CO₂ equivalents,Other\n")
                f.write("2000,30000,foo\n")
                f.write("2001,31000,bar\n")

            # Bytt til temp data dir under test
            original_cwd = os.getcwd()
            os.chdir(tmpdir)

            try:
                run_rensing.rens_og_lagre_klimagass_verden()

                self.assertTrue(os.path.exists(output_path))
                df = pd.read_csv(output_path)

                self.assertIn("År", df.columns)
                self.assertIn("Utslipp i CO2 ekvivalenter", df.columns)
                self.assertEqual(df.shape, (2, 2))
                self.assertEqual(df["Utslipp i CO2 ekvivalenter"].iloc[1], 31000)

            finally:
                os.chdir(original_cwd)
        
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