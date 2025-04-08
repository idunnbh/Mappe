import pandas as pd
import numpy as np
import json

def analyser_fil(filsti, sep=',', datokolonne=None, groupby='måned'):
    df = pd.read_csv(filsti, sep=sep) # Leser inn CSV-data
    df.columns = df.columns.str.strip().str.replace('"', '').str.lower()  # Rens kolonnenavn
    print(f"\nAnalyse av:{filsti}")
    print("-------------------------------------------------")

    grupper = []
    statistikk = {}


    if datokolonne:
        datokolonne = datokolonne.strip().lower() # Fikser datokolonnen
        if datokolonne not in df.columns:
            print("Datokolonnen IKKE funnet.")
            return
    else: 
        print("Datokolonne ikke spesifisert (Hopper over gruppering).")
        return

    # Behandler dato og/eller årstall
    if pd.api.types.is_integer_dtype(df[datokolonne]):
        df['år'] = df[datokolonne]
        grupper = ['år']
    else:
        df[datokolonne] = pd.to_datetime(df[datokolonne], errors='coerce')
        df['år'] = df[datokolonne].dt.year
        if groupby == 'år':
            grupper = ['år']
        elif groupby == 'måned':
            df['måned'] = df[datokolonne].dt.month
            grupper = ['år', 'måned']
        else:
            print("Ukjent groupby-verdi. Bruk 'år' eller 'måned'.")
            return

    if not grupper:
        print("Kan ikke gruppere. Hopper over analyse.")
        return

    # Finn numeriske kolonner
    numeriske_kolonner = df.select_dtypes(include=[np.number]).columns.difference(['år', 'måned'])

    # Grupper etter måned (hvis spesisfisert)
    if groupby == 'måned':
        for kol in numeriske_kolonner:
            #print(f"\nStatistikk for kolonne: {kol} (gruppert etter år og måned)")
            stats = df.groupby(['år', 'måned'])[kol].agg(['mean', 'median', 'std']).reset_index()
            #print(stats.round(2))
            statistikk[f"{kol}_måned"] = stats

    # Grupper etter år (alltid)
    for kol in numeriske_kolonner:
        #print(f"\nStatistikk for kolonne: {kol} (gruppert etter år)")
        stats = df.groupby('år')[kol].agg(['mean', 'median', 'std']).reset_index()
        #print(stats.round(2))
        statistikk[f"{kol}_år"] = stats

    return statistikk

def json_til_dataframe(json_fil, tidspunkt="from"):
    
    with open(json_fil, encoding="utf-8") as fil:
        innhold = json.load(fil)

    rader = []
    tid = innhold.get("data", {}).get("time", [])

    for målepunkt in tid:
        rad = {"tidspunkt": målepunkt.get(tidspunkt)}
        for komponent, verdi in målepunkt.get("variables", {}).items():
            rad[komponent] = verdi.get("value")
        rader.append(rad)

    return pd.DataFrame(rader)