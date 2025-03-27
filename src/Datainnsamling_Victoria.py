import pandas as pd 
import matplotlib.pyplot as plt       # For diagram senere
import os

    # Finne CSV og definere ; som seperator, df = dataframe/tabell i pandas
base_path = os.path.dirname(__file__)
file_path = os.path.join(base_path, "../data/klimagassutslipp_renset.csv")
df = pd.read_csv(file_path, sep=",", encoding="utf-8")

    # Definere at vi kun vil se "0 Alle kilder" og "Klimagasser i alt" fra CSVen, kan endres
df = df[(df["kilde (aktivitet)"] == "0 Alle kilder") & (df["komponent"] == "Klimagasser i alt")]

    # Konvertere år og utslipp fra streng til tall, "coerce" gjør noe som ikke kan gjøres om til tall -> NaN istedet for å kræsje, 
df["år"] = pd.to_numeric(df["år"], errors = "coerce")
df["Utslipp til luft (1 000 tonn CO2-ekvivalenter, AR5)"] = pd.to_numeric(
    df["Utslipp til luft (1 000 tonn CO2-ekvivalenter, AR5)"], errors = "coerce"
)

    # Test
print(df.head())