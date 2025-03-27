import pandas as pd
import os
from databehandling.rensing_temperaturdata import rens_data, klimagass_rens

df_temp = pd.read_csv("data/gloshaugen_temperaturer.csv")

#Renser data
df_temp = rens_data(df_temp)

#Lager er renset csv fil 
df_temp.to_csv("data/temperatur_renset.csv", index=False)
print("Renset data lagret i data/temperatur_renset.csv")

    # Kaller CSV om klimagassutslipp og renser den
klimagass_renset_path = "data/klimagassutslipp_renset.csv"

if not os.path.exists(klimagass_renset_path):
    df_klima = pd.read_csv("data/klimagassutslipp.csv", sep=";", encoding="utf-8", skiprows=2)
    df_klima = klimagass_rens(df_klima)
    df_klima.to_csv("data/klimagassutslipp_renset.csv", index=False)
    print("Renset data lagret i data/klimagassutslipp_renset.csv")
else:
    print("Klimagassdata er allerede renset.")