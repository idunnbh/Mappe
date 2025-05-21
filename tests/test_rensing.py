import os
import sys
import unittest

import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import rensing

class TestRensing(unittest.TestCase):

#Positiv test: Sjekker at funksjonene fungerer som forventet under normale forhold.
    def test_fjern_outliers_positive(self):
        "Skal fjerne utlier (100) og beholde resten"
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
        "Skal fylle manglende verdi med gjennomsnitt (15)"
        data = {'temperatur': [10, None, 20]}
        df = pd.DataFrame(data)
        df = rensing.håndter_manglende_verdier(df)
        
        self.assertFalse(df['temperatur'].isnull().any())
        self.assertEqual(df['temperatur'].iloc[1], 15.0)  

    def test_fjern_duplikater(self):
        "Skal fjerne dobble tidspunkter "
        data = {'tidspunkt': ['2025-01-01 12:00', '2025-01-01 12:00'], 'temperatur': [5.0, 5.0]}
        df = pd.DataFrame(data)
        df = rensing.fjern_duplikater(df)
        self.assertEqual(len(df), 1)
    
    #Positiv test for rensing av kolonnenavn
    def test_rense_kolonnenavn(self):
        "Skal rense kolonnenavn"
        data = {
            '"år"': [],
            '"komponent"': [],
            '"verdi"': []
        }
        df = pd.DataFrame(data)
        df_renset = rensing.rense_kolonnenavn(df)
        self.assertListEqual(list(df_renset.columns), ['år', 'komponent', 'verdi'])

    def test_rense_luftkvalitet(self):
        "Skal fjerne rader med lav dekning og sette negative verdier til 0"
        data = {
            "Dekning": [85.0, 60.0],
            "Dekning.1": [90.0, 90.0],
            "Dekning.2": [90.0, 90.0],
            "Elgeseter NO2 µg/m³ Day": ["-5,0", "10,0"],
            "Elgeseter PM10 µg/m³ Day": ["15,0", "-20,0"],
            "Elgeseter PM2.5 µg/m³ Day": ["25,0", "30,0"],
        }
        df = pd.DataFrame(data)
        renset_df = rensing.rense_luftkvalitet(df)

        # Bare første rad har høy nok dekning og skal bli igjen
        self.assertEqual(len(renset_df), 1)

        # Negative verdier skal ha blit satt til 0
        self.assertEqual(renset_df["Elgeseter NO2 µg/m³ Day"].iloc[0], 0.0)
        self.assertEqual(renset_df["Elgeseter PM10 µg/m³ Day"].iloc[0], 15.0)
        self.assertEqual(renset_df["Elgeseter PM2.5 µg/m³ Day"].iloc[0], 25.0)

    
if __name__ == '__main__':
    unittest.main()