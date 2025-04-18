import requests
import csv
import os
from datetime import datetime
import pytz
import pandas as pd
from dotenv import load_dotenv
from datetime import date

#Hente API-nøkler fra .env 
load_dotenv('api.env')
USER_AGENT = os.getenv('USER_AGENT')
FROST_API_KEY = os.getenv('FROST_API_KEY')

#Hent sanntidsdata fra MET
def hent_sanntidsdata(lat, lon):
    if not USER_AGENT:
        raise ValueError("USER_AGENT mangler! Sjekk api.env")

    url = f'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={lat}&lon={lon}'
    headers = {'User-Agent': USER_AGENT}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Sanntidsdata hentet!")
        return response.json()
    else:
        print(f"Feil ved henting av sanntidsdata: {response.status_code}")
        return None

def hent_temperaturer(data):
    temperaturer = []
    for timepunkt in data['properties']['timeseries']:
        tid = timepunkt['time']
        temp = timepunkt['data']['instant']['details']['air_temperature']
        temperaturer.append((tid, temp))
    return temperaturer

#Henter historiske temperaturdata fra Frost API
def hent_historiske_temperaturer(antall_år=50):
    if not FROST_API_KEY:
        raise ValueError("FROST_API_KEY mangler! Sjekk api.env")
    
    endpoint = "https://frost.met.no/observations/v0.jsonld"
    temperaturer = []

    sluttår = datetime.now().year
    startår = sluttår - antall_år + 1
     # For å unngå ufullstendig måned
    sluttmåned = datetime.now().month - 1 if datetime.now().day < 28 else datetime.now().month 

    if sluttmåned == 0:
        sluttmåned = 12
        sluttår -= 1


    for år in range(startår, sluttår + 1):
        for måned in range(1, 13):
            if år == sluttår and måned > sluttmåned:
                break
            startdato = f"{år}-{måned:02d}-01"
            if måned == 12:
                sluttdato = f"{år}-12-31"
            else:
                sluttdato = f"{år}-{måned + 1:02d}-01"

            params = {
                "sources": "SN18700",  # Gløshaugen
                "elements": "air_temperature",
                "referencetime": f"{startdato}/{sluttdato}",
            }

            response = requests.get(endpoint, params=params, auth=(FROST_API_KEY, ''))

            if response.status_code == 200:
                print(f"Data hentet for {startdato} til {sluttdato}")
                data = response.json()
                for obs in data["data"]:
                    tidspunkt = obs["referenceTime"]
                    verdi = obs["observations"][0]["value"]
                    temperaturer.append((tidspunkt, verdi))
            else:
                print(f"Feil ved {startdato}/{sluttdato}: {response.status_code}")
     
    #Behold kun en måling per time:
    df = pd.DataFrame(temperaturer, columns=["tidspunkt", "temperatur"])
    df["tidspunkt"] = pd.to_datetime(df["tidspunkt"])
    df = df.set_index("tidspunkt").resample("1h").first().dropna().reset_index()

    # Gjør om tilbake til liste 
    return list(df.itertuples(index=False, name=None))


#Lagrer listene til csv filer 
def lagre_til_csv(data, filnavn):
    os.makedirs('data', exist_ok=True)
    with open(f'data/{filnavn}', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['tidspunkt', 'temperatur'])
        writer.writerows(data)
    print(f"Tempraturdata er nå lagret i data/{filnavn}")


def main():
    lat, lon = 63.4195, 10.4065  # Gløshaugen, Trondheim
    today = date.today().isoformat()
    antall_år=50

    # Sanntidsdata, 48 neste timene. Genererer ny hver gang
    filnavn=f"temp_gloshaugen_sanntid_{today}.csv"
    sanntidsdata = hent_sanntidsdata(lat, lon)
    
    if sanntidsdata:
        temp_sanntid = hent_temperaturer(sanntidsdata)
        lagre_til_csv(temp_sanntid, filnavn)

    # Historiske data hvis den ikke finnes fra før
    filnavn = f"temp_gloshaugen_historisk_{antall_år}år.csv"
    filsti = f"data/{filnavn}"
    if not os.path.exists(filsti):
        temp_historisk = hent_historiske_temperaturer(antall_år)
        lagre_til_csv(temp_historisk, filnavn)
    else:
        print("Historisk temperaturdata er allerede lagret under data")    

if __name__ == "__main__":
    main()
