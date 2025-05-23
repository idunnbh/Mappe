import os
from datetime import date

import pandas as pd

from datainnsamling_temperatur import main as hent_temperaturdata_main
from rensing import temperatur_rens, klimagass_rens, rense_luftkvalitet


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

# Kaller CSV om klimagassutslipp i norge og renser den
def rens_og_lagre_klimagassdata_norge():
    klimagass_renset_path = "data/klimagassutslipp_norge_renset.csv"
    if not os.path.exists(klimagass_renset_path):
        df_klima = pd.read_csv("data/klimagassutslipp.csv", sep=";", encoding="utf-8", skiprows=2)
        df_klima = klimagass_rens(df_klima)
        df_klima.to_csv("data/klimagassutslipp_norge_renset.csv", index=False)
        print("Renset data lagret i data/klimagassutslipp_norge_renset.csv")
    else:
        print("Klimagassdata er allerede renset.")

# Kaller CSV om verdens klimagassutslipp og renser den
def rens_og_lagre_klimagass_verden():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists("data/klimagassutslipp_verden.csv"):
        print("Fant ikke filen: data/klimagassutslipp_verden.csv")
        return
    df = pd.read_csv("data/klimagassutslipp_verden.csv")
    df.rename(columns={
        "Year": "År",
        "Annual greenhouse gas emissions in CO₂ equivalents": "Utslipp i CO2 ekvivalenter"
    }, inplace=True)
    df_renset = df[["År", "Utslipp i CO2 ekvivalenter"]]
    df_renset.to_csv("data/klimagassutslipp_verden_renset.csv", index=False)
    print("Renset data lagret i data/klimagassutslipp_verden_renset.csv")

def rens_og_lagre_luftkvalitet():
    os.makedirs("data", exist_ok=True)
    historisk_csv = "data/historisk_luftkvalitet.csv"
    renset_csv = "data/gyldig_historisk_luftkvalitet.csv"

    if os.path.exists(renset_csv):
        print("Historisk luftkvalitetsdata er allerede renset.")
        print("Renset data lagret i data/data/gyldig_historisk_luftkvalitet.csv")
        return
    
    if not os.path.exists(historisk_csv):
        print(f"Fant ikke filen: {historisk_csv}")
        return

    df = pd.read_csv(historisk_csv, sep=",")
   
    cols = [
        "Elgeseter NO2 µg/m³ Day",
        "Elgeseter PM10 µg/m³ Day",
        "Elgeseter PM2.5 µg/m³ Day",
    ]
    
    df = rense_luftkvalitet(df)

    for col in cols:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", "."), errors="coerce")
        df[col] = df[col].clip(lower=0)

    df.to_csv(renset_csv, index=False, encoding="utf-8")
    print(f"Renset luftkvalitetsdata lagret i {renset_csv}")

if __name__ == "__main__":
    try:
        hent_temperaturdata_main()
    except ValueError as e:
        if "USER_AGENT" in str(e):
            print("USER_AGENT mangler. Henter ikke sanntidsdata for temperatur.")
        else:
            raise
    rens_og_lagre_temperaturdata()
    rens_og_lagre_klimagassdata_norge()
    rens_og_lagre_klimagass_verden()
    rens_og_lagre_luftkvalitet()