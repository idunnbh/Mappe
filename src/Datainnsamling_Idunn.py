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


#Normaliserer JSON-strukturen til en Pandas DataFrame
def process_air_quality_data(data):
    try:
        df = pd.json_normalize(data, record_path=["data", "time"])
        df.ffill(inplace=True) #Fyller inn manglende verdier med forrige verdi
        return df
    except Exception as e:
        raise Exception(f"Feil ved behandling av data: {e}")
    

# Hent data fra API-et
air_quality_data = get_air_quality_data(met_url, params, headers)
# Lagre data til JSON-fil
save_json_data(air_quality_data, "data/luftkvalitet.json")
# Bearbeid dataene med Pandas
df = process_air_quality_data(air_quality_data)
#print("Første 5 rader av den bearbeidede DataFrame:")
print(df.head())



