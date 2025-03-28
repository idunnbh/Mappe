import pandas as pd
from datetime import date
import os
from databehandling.rensing import temperatur_rens, klimagass_rens

def rens_og_lagre_temperaturdata():
    os.makedirs("data", exist_ok=True)
    #Sanntids temperaturer 
    today = date.today().isoformat()
    sanntid_csv = f"data/temp_gloshaugen_sanntid_{today}.csv"
    sanntid_renset = f"data/temp_gloshaugen_sanntid_{today}_renset.csv"
    if os.path.exists(sanntid_csv):
        df = pd.read_csv(sanntid_csv)
        df = temperatur_rens(df)
        df.to_csv(sanntid_renset, index=False)
        print(f"Sanntidstemperaturer renset og lagret: {sanntid_renset}")
    else:
        print(f"Fant ikke sanntidsdata for temperatur: {sanntid_csv}")

    #Historisk
    hist_csv = "data/temp_gloshaugen_historisk.csv"
    hist_renset = "data/temp_gloshaugen_historisk_renset.csv"
    if not os.path.exists(hist_renset) and os.path.exists(hist_csv):
        df = pd.read_csv(hist_csv)
        df = temperatur_rens(df)
        df.to_csv(hist_renset, index=False)
        print("Historisk temperaturdata renset.")
    elif os.path.exists(hist_renset):
        print("Historisk temperaturdata allerede renset.")
    else:
        print("Fant ikke historisk temperaturdata.")

# Kaller CSV om klimagassutslipp og renser den
def rens_og_lagre_klimagassdata():
    klimagass_renset_path = "data/klimagassutslipp_renset.csv"
    if not os.path.exists(klimagass_renset_path):
        df_klima = pd.read_csv("data/klimagassutslipp.csv", sep=";", encoding="utf-8", skiprows=2)
        df_klima = klimagass_rens(df_klima)
        df_klima.to_csv("data/klimagassutslipp_renset.csv", index=False)
        print("Renset data lagret i data/klimagassutslipp_renset.csv")
    else:
        print("Klimagassdata er allerede renset.")

if __name__ == "__main__":
    rens_og_lagre_temperaturdata()
    rens_og_lagre_klimagassdata()