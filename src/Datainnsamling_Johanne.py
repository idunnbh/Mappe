import requests
import csv
import os
from datetime import datetime
import pytz
import pandas as pd
from pandasql import sqldf
from dotenv import load_dotenv

# Henter User-Agent fra api.env
load_dotenv('api.env')
USER_AGENT = os.getenv('USER_AGENT')

# Hente værdata fra Yr/MET API
def hent_weather_data(lat, lon):
    url = f'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={lat}&lon={lon}'
    headers = {'User-Agent': USER_AGENT}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print("Velykket henting av data!")
        return response.json() 
    else:
        print(f"Feil ved henting av data!")
        print(f"Feil kode:{response.status_code}")
        return None

# Henter ut temperaturer fra JSON
def hent_temperaturer(data):
    temperaturer = []
    for timepunkt in data['properties']['timeseries']:
        tid = timepunkt['time']
        temp = timepunkt['data']['instant']['details']['air_temperature']
        temperaturer.append((tid, temp))
    return temperaturer

# Lagrer data til CSV
def lagre_til_csv(data, filnavn):
    os.makedirs('data', exist_ok=True)  # Lager data-mappe hvis den ikke finnes
    with open(f'data/{filnavn}', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['tidspunkt', 'temperatur'])
        writer.writerows(data)
    print(f'Data lagret i data/{filnavn}')

if __name__ == "__main__":
    # Koordinater for Gløshaugen, Trondheim
    lat, lon = 63.4195, 10.4065
    weather_data = hent_weather_data(lat, lon)

    if weather_data:
        temperaturer = hent_temperaturer(weather_data)
        lagre_til_csv(temperaturer, 'gloshaugen_temperaturer.csv')
    
  