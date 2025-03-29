import unittest
import pandas as pd
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import rensing

class TestRensing(unittest.TestCase):

#Positiv test: Sjekker at funksjonene fungerer som forventet under normale forhold.
    def test_fjern_outliers_positive(self):
        data = {'temperatur': [-5, 5, 100, 20]}  #100 er en outlier
        df = pd.DataFrame(data)
        renset_df = rensing.fjern_outliers(df)
        self.assertEqual(len(renset_df), 3)

#Negativ test: Sjekker at funksjonene håndterer uvanlige/ekstreme tilfeller. 
    def test_fjern_outliers_negative(self):
        data = {'temperatur': [1000]}  #alle er outliers
        df = pd.DataFrame(data)
        renset_df = rensing.fjern_outliers(df)
        self.assertEqual(len(renset_df), 0)

    def test_håndter_manglende_verdier(self):
        data = {'temperatur': [10, None, 20]}
        df = pd.DataFrame(data)
        df = rensing.håndter_manglende_verdier(df)
        self.assertFalse(df['temperatur'].isnull().any())

    def test_fjern_duplikater(self):
        data = {'tidspunkt': ['2025-01-01 12:00', '2025-01-01 12:00'], 'temperatur': [5.0, 5.0]}
        df = pd.DataFrame(data)
        df = rensing.fjern_duplikater(df)
        self.assertEqual(len(df), 1)
    
    def test_temperatur_rens_kombinert(self):
        data = {
            'tidspunkt': ['2025-01-01 12:00', '2025-01-01 12:00'],
            'temperatur': [None, 1000]  # én mangler, én outlier og duplikat
        }
        df = pd.DataFrame(data)
        df_renset = rensing.temperatur_rens(df)
        self.assertEqual(len(df_renset), 0)

if __name__ == '__main__':
    unittest.main()
