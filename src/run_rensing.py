import pandas as pd
from databehandling.rensing_temperaturdata import rens_data, klimagass_rens

df_temp = pd.read_csv("data/gloshaugen_temperaturer.csv")

#Renser data
df_temp = rens_data(df)

#Lager er renset csv fil 
df_temp.to_csv("data/temperatur_renset.csv", index=False)
print("Renset data lagret i data/temperatur_renset.csv")


    # Kaller CSV om klimagassutslipp og renser den
df_klima = pd.read_csv("data/klimagassutslipp.csv", sep=";", encoding="utf-8", skiprows=2)
df_temp = klimagass_rens
df_temp.to_csv("data/klimagassutslipp_renset.csv", index=False)
print("Renset data lagret i data/klimagassutslipp_renset.csv")