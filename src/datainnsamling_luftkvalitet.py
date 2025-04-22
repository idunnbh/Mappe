import requests
import json
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv('api.env')
my_user_agent = os.getenv("IDUNN_USER_AGENT")
met_url = os.getenv("MET_API_URL")

params = {
    "lat": "63.4195",   #Koordinater for Gløshaugen, Trondheim
    "lon": "10.4065"
}
headers = {"User-Agent": my_user_agent}


def get_air_quality_data(url, params, headers):
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Feil ved henting av data: {response.status_code}")
    

def save_json_data(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Data lagret til {filename}")


# Normaliserer JSON-strukturen til en Pandas DataFrame
def process_air_quality_data(data):
    try:
        df = pd.json_normalize(data, record_path=["data", "time"])
        return df
    except Exception as e:
        raise Exception(f"Feil ved behandling av data: {e}")
    

# Hent data fra API-et
air_quality_data = get_air_quality_data(met_url, params, headers)
# Lagre data til JSON-fil
save_json_data(air_quality_data, "data/luftkvalitet.json")
# Bearbeid dataene med Pandas
df = process_air_quality_data(air_quality_data)


# Leser fra luftkvalitet.json
with open("data/luftkvalitet.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# Lagrer den normaliserte dataframen i varaiabelen df
df = process_air_quality_data(raw_data)
    
# Velger ut hvilke konsentrasjoner fra API-en vi analyserer videre
selected_columns = [
    "from",
    "to",
    "variables.pm10_concentration.value",
    "variables.pm25_concentration.value",
    "variables.no2_concentration.value",
]
df_selected = df[selected_columns].copy()   #Ny dataframe df_selected med de utvalgte verdiene

# Lagrer se utvalgte verdiene som ny CSV-fil
df_selected.to_csv("data/luftkvalitet_api.csv", index=False, encoding="utf-8")


# Henter historisk data fra Norsk institutt for luftforskning, lagret som CSV-fil lokalt på min pc
df_historisk = pd.read_csv(r"C:\Users\idunn\OneDrive - NTNU\TDT4114\luftkvalitet_20aar.csv", sep=";", skiprows=3)
df_historisk.to_csv("data/historisk_luftkvalitet.csv", index=False, encoding="utf-8")


# Datasettet er veldig mangelfullt, så ekskluderer radene som har for lav dekning
df_valid = df_historisk[
    (df_historisk["Dekning"] >= 80.0) &
    (df_historisk["Dekning.1"] >= 80.0) &
    (df_historisk["Dekning.2"] >= 80.0)
].copy()


cols = [
    "Elgeseter NO2 µg/m³ Day",
    "Elgeseter PM10 µg/m³ Day",
    "Elgeseter PM2.5 µg/m³ Day",
]

# Først erstatt komma med punktum og konverter til float
df_valid["Elgeseter NO2 µg/m³ Day"] = df_valid["Elgeseter NO2 µg/m³ Day"].str.replace(',', '.').astype(float)
df_valid["Elgeseter PM10 µg/m³ Day"] = df_valid["Elgeseter PM10 µg/m³ Day"].str.replace(',', '.').astype(float)
df_valid["Elgeseter PM2.5 µg/m³ Day"] = df_valid["Elgeseter PM2.5 µg/m³ Day"].str.replace(',', '.').astype(float)


# Sett alle negative verdier i disse kolonnene til 0
df_valid.loc[:, cols] = df_valid.loc[:, cols].clip(lower=0)

# Lagrer gyldige verdier som ny CSV-fil
df_valid.to_csv("data/gyldig_historisk_luftkvalitet.csv", index=False, encoding="utf-8")

