import requests
import json
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import date

def hent_siste_reftime():
    headers = {"User-Agent": os.getenv("USER_AGENT")}
    url = "https://api.met.no/weatherapi/airqualityforecast/0.1/reftimes"

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Feil ved henting av reftime: {response.status_code}")
    
    reftimes = response.json()["reftimes"]
    return reftimes[-1]

def hent_sanntids_luftkvalitet():
    load_dotenv('api.env')
    station = "NO0057A"
    my_user_agent = os.getenv("USER_AGENT")
    if not my_user_agent:
        raise ValueError("USER_AGENT mangler! Sjekk api.env")

    headers = {"User-Agent": my_user_agent}
    reftime = hent_siste_reftime()
    url = f"https://api.met.no/weatherapi/airqualityforecast/0.1/?station={station}&reftime={reftime}"

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Feil ved henting av data: {response.status_code}")
    
    data = response.json()
    df = pd.json_normalize(data, record_path=["data", "time"])

    selected_columns = [
        "from",
        "to",
        "variables.pm10_concentration.value",
        "variables.pm25_concentration.value",
        "variables.no2_concentration.value",
    ]
    df = df[selected_columns].copy()
    df["from"] = pd.to_datetime(df["from"]) 
    return df


def hent_historisk_luftkvalitet(filsti: str) -> pd.DataFrame:
    df = pd.read_csv(filsti, sep=",")
    df.columns = df.columns.str.strip()  
    
    # Datasettet er veldig mangelfullt, så ekskluderer radene som har for lav dekning
    df = df[
    (df["Dekning"] >= 80.0) &
    (df["Dekning.1"] >= 80.0) &
    (df["Dekning.2"] >= 80.0)
    ].copy()
    
    # Kolonner som skal konverteres
    cols = [
    "Elgeseter NO2 µg/m³ Day",
    "Elgeseter PM10 µg/m³ Day",
    "Elgeseter PM2.5 µg/m³ Day",
    ]

    for col in cols:
        df[col] = df[col].str.replace(",", ".").astype(float)
        # Sett alle negative verdier i disse kolonnene til 0
        df[col] = df[col].clip(lower=0)
    
    return df

def lagre_til_csv(df: pd.DataFrame, filnavn: str):
    df.to_csv(filnavn, index=False, encoding="utf-8")
    print(f"Data lagret til {filnavn}")


def lagre_luftkvalitetsdata(filsti):
    today = date.today().isoformat()

    filnavn_sanntid = f"luftkvalitet_sanntid_{today}.csv"
    df_api = hent_sanntids_luftkvalitet()
    df_api.to_csv(f"data/{filnavn_sanntid}", index=False, encoding="utf-8")
    print(f"Sanntidsdata lagret som data/{filnavn_sanntid}")

    filnavn_hist = f"luftkvalitet_historisk.csv"
    full_filsti = f"data/{filnavn_hist}"

    if not os.path.exists(full_filsti):
        df_hist = hent_historisk_luftkvalitet(filsti)
        df_hist.to_csv(full_filsti, index=False, encoding="utf-8")
        print(f"Historisk data lagret som {filnavn_hist}")
    else:
        print("Historisk luftkvalitetsdata er allerede lagret.")

if __name__ == "__main__":
    lagre_luftkvalitetsdata("data/historisk_luftkvalitet.csv")
