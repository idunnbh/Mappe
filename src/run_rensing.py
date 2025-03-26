import pandas as pd
from databehandling.rensing_temperaturdata import rens_data

df = pd.read_csv("data/gloshaugen_temperaturer.csv")

#Renser data
df = rens_data(df)

#Lager er renset csv fil 
df.to_csv("data/temperatur_renset.csv", index=False)
print("Renset data lagret i data/temperatur_renset.csv")
