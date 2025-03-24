import requests
from dotenv import load_dotenv 
import os

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


if __name__ == "__main__":
    # Koordinater for Gløshaugen, Trondheim
    lat, lon = 63.4195, 10.4065

    weather_data = hent_weather_data(lat, lon)
    
  