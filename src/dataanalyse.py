import pandas as pd
import numpy as np
import json

def analyser_fil(filsti, sep=',', datokolonne=None, groupby='måned'):
    df = pd.read_csv(filsti, sep=sep) # Leser inn CSV-data
    df.columns = df.columns.str.strip().str.replace('"', '').str.lower()  # Rens kolonnenavn
    df.columns = df.columns.str.replace(" ", "_").str.replace("µg/m³", "ugm3").str.replace("ug/m3", "ugm3") 
    print(f"\nAnalyse av:{filsti}")
    print("-------------------------------------------------")

    if datokolonne:
        datokolonne = datokolonne.strip().lower() # Fikser datokolonnen
        if datokolonne not in df.columns:
            print("Datokolonnen IKKE funnet.")
            return
    else: 
        print("Datokolonne ikke spesifisert (Hopper over gruppering).")
        return
    
    grupper = []

    # Beholder dato eller årstall
    if pd.api.types.is_integer_dtype(df[datokolonne]):
        df['år'] = df[datokolonne]
    else:
        df[datokolonne] = pd.to_datetime(df[datokolonne], errors='coerce')
        df['år'] = df[datokolonne].dt.year
        if groupby == 'måned':
            df['måned'] = df[datokolonne].dt.month

    # Gruppering
    grupper = ['år']  
    if groupby == 'måned':
        grupper.append('måned')

    if 'kilde (aktivitet)' in df.columns:
        grupper.insert(0, 'kilde (aktivitet)') # Grupperer først mhp. kilde
    
    if not grupper:
        print("Kan ikke gruppere. Hopper over analyse.")
        return

    # Finner numeriske kolonner
    numeriske_kolonner = df.select_dtypes(include=[np.number]).columns.difference(['år', 'måned'])
    # Fjerner kolloner som starter med dekning (mhp på vidre analyse av luftkvalitetdata)
    filtrerte_kolonner = []
    for kol in numeriske_kolonner:
        if not kol.lower().startswith("dekning"):
            filtrerte_kolonner.append(kol)

    numeriske_kolonner = filtrerte_kolonner

    statistikk = {}

    # Grupper etter år
    for kol in numeriske_kolonner:
        gruppe_størrelser = df.groupby(grupper).size()

        # Sjekk om det er nok datapunkter til å beregne standardavvik
        if gruppe_størrelser.min() > 1:
            stats = df.groupby(grupper)[kol].agg(['mean', 'median', 'std']).reset_index()
        else:
        # Bare mean og median
            stats = df.groupby(grupper)[kol].agg(['mean', 'median']).reset_index()

        stats = stats.rename(columns={
            'mean': 'gjennomsnitt',
            'median': 'median',
            'std': 'standardavvik'
        })
        statistikk[kol] = stats

    return statistikk
