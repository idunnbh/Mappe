import os
import sys
from pathlib import Path
import unittest

import pandas as pd
from dotenv import load_dotenv

# Legg til src-mappa i system path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

# Last inn miljøvariabler
load_dotenv()

from datainnsamling_luft import (
    hent_siste_reftime,
    hent_sanntids_luftkvalitet,
    hent_historisk_luftkvalitet,
    lagre_til_csv
)

class TestDatainnsamlingLuftEkte(unittest.TestCase):

    def test_hent_siste_reftime_ekte(self):
        ref = hent_siste_reftime()
        self.assertTrue(ref.startswith("202"), "Reftime ser ikke ut som en dato")

    def test_hent_sanntids_luftkvalitet_ekte(self):
        df = hent_sanntids_luftkvalitet()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertIn("from", df.columns)
        self.assertFalse(df.empty, "DataFrame er tom")

    def test_hent_historisk_luftkvalitet(self):
        path = Path("data/historisk_luftkvalitet.csv")
        self.assertTrue(path.exists(), "Filen for historisk luftkvalitet mangler")
        df = hent_historisk_luftkvalitet(str(path))
        self.assertFalse(df.empty, "Historisk data er tom")
        self.assertIn("Elgeseter NO2 µg/m³ Day", df.columns)


    def test_lagre_til_csv(self):
        df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
        filnavn = "data/test_luft.csv"
        lagre_til_csv(df, filnavn)
        self.assertTrue(Path(filnavn).exists())
        Path(filnavn).unlink()

if __name__ == "__main__":
    unittest.main()

