import pandas as pd
from datetime import date
import os
from rensing import temperatur_rens, klimagass_rens

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
        print(f"Sanntidstemperaturer renset og lagret i: {sanntid_renset}")
    else:
        print(f"Fant ikke sanntidsdata for temperatur: {sanntid_csv}")

    #Historisk data(ekte)
    antall_år = 50
    hist_csv_normal = f"data/temp_gloshaugen_historisk_{antall_år}år.csv"
    hist_renset_normal = f"data/temp_gloshaugen_historisk_renset_ {antall_år}.csv"

    if os.path.exists(hist_renset_normal):
        print("Historisk temperaturdata er allerede renset.")
    elif os.path.exists(hist_csv_normal):
        df = pd.read_csv(hist_csv_normal)
        df = temperatur_rens(df)
        df.to_csv(hist_renset_normal, index=False)
        print(f"Historisk temperaturdata renset og lagret i:{hist_renset_normal}")
    else:
        print("Fant ikke historisk temperaturdata")

    #Historisk data med feil
    hist_csv_feil = f"data/temp_gloshaugen_historisk_inneholder_feil_{antall_år}år.csv"
    hist_renset_feil = f"data/temp_gloshaugen_historisk_inneholder_feil_renset_{antall_år}år.csv"

    if os.path.exists(hist_renset_feil):
        print("Historisk temperaturdata med feil er allerede renset.")
    elif os.path.exists(hist_csv_feil):
        df = pd.read_csv(hist_csv_feil)
        df = temperatur_rens(df)
        df.to_csv(hist_renset_feil, index=False)
        print(f"Historisk temperaturdata(med feil) renset lagret i:{hist_renset_feil}")
    else:
        print("Fant ikke historisk temperaturdata (med feil)")

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