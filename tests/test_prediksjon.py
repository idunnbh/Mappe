import os
import sys
import unittest

import numpy as np
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from prediksjon import regresjonsmodell


class TestRegresjonsmodell(unittest.TestCase):

    def test_regresjonsmodell_lineære_data(self):
        df = pd.DataFrame({
            "år": [2000, 2005, 2010, 2015, 2020],
            "temp": [5.0, 5.5, 6.0, 6.5, 7.0]
        })

        X = df[["år"]]
        y = df["temp"]

        modell, r2, mse = regresjonsmodell(X, y)

        # R2 bør være ca. 1.0 for perfekt lineær sammenheng
        self.assertAlmostEqual(r2, 1.0, places=2)

        # MSE bør være veldig lavt
        self.assertLess(mse, 1e-10)

        # Stigningstall bør være ca 0.1 (1 grad per 10 år)
        self.assertAlmostEqual(modell.coef_[0], 0.1, places=2)

        # Intercept bør være nær -195
        pred_2000 = modell.predict(pd.DataFrame([[2000]], columns=["år"]))
        self.assertAlmostEqual(pred_2000, 5.0, places=1)

if __name__ == "__main__":
    unittest.main()
