import pandas as pd
from pandasql import sqldf

def last_in_csv(filsti):
    return pd.read_csv(filsti)

def finn_gjennomsnittstemperatur(df):
    pysqldf = lambda q: sqldf(q, {'df': df})
    query = "SELECT AVG(temperatur) as snitt_temp FROM df WHERE temperatur IS NOT NULL"
    result = pysqldf(query)
    return result['snitt_temp'].iloc[0]

def håndter_manglende_verdier(df, kolonne='temperatur'):
    manglende_verdi= df[df[kolonne].isnull()]
    print(f"Manglende verdier = {len(manglende_verdi)}")

    for i in manglende_verdi.index:
        if 0 < i < len(df) - 1:
            før = df.loc[i - 1, kolonne]
            etter = df.loc[i + 1, kolonne]

            if pd.notnull(før) and pd.notnull(etter):
                gjennomsnitt = (før + etter) / 2
                df.at[i, kolonne] = gjennomsnitt
                print(f"Fylte inn gjennomsnitt: {gjennomsnitt}, (mellom {før} og {etter})")
            else:
                print(f"Kunne ikke fylle inn verdi")
        else:
            print(f"Kunne ikke fylle inn verdi")

    return df


def fjern_duplikater(df):
    før = len(df)
    df = df.drop_duplicates()
    etter = len(df)
    print(f"Fjernet {før - etter} duplikater.")
    return df

def fjern_outliers(df, min_temp=-50, max_temp=50):
    outliers = df[(df['temperatur'] < min_temp) | (df['temperatur'] > max_temp)]
    antall = len(outliers)
    if not outliers.empty:
        for idx, row in outliers.iterrows():
            print(f"Outlier på rad {idx}: temperatur = {row['temperatur']}")
    df = df[(df['temperatur'] >= min_temp) & (df['temperatur'] <= max_temp)]
    
    print(f"Fjernet {antall} outliers.")
    return df

def rense_kolonnenavn(df):
    df.columns = df.columns.str.replace('"', '').str.strip()
    return df    

def temperatur_rens(df):
    df = håndter_manglende_verdier(df)
    df = fjern_duplikater(df)
    df = fjern_outliers(df)
    return df

def klimagass_rens(df):
    df = rense_kolonnenavn(df)
    
    nødvendige_kolonner = ['kilde (aktivitet)', 'komponent', 'år']
    for kol in nødvendige_kolonner:
        if kol not in df.columns:
            raise KeyError (f"Mangler nødvendig kolonne: '{kol}'")
        
    df = fjern_duplikater(df)
    return df

def rense_luftkvalitet(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.strip()
    rader_før = len(df)
    # Datasettet er veldig mangelfullt, så ekskluderer radene som har for lav dekning
    df = df[
        (df["Dekning"] >= 80.0) &
        (df["Dekning.1"] >= 80.0) &
        (df["Dekning.2"] >= 80.0)
    ].copy()
    rader_etter = len(df)
    fjernet_rader = rader_før - rader_etter
    print(f"Fjernet {fjernet_rader} rader pga. lav dekning.")

    # Kolonner som skal konverteres
    cols = [
        "Elgeseter NO2 µg/m³ Day",
        "Elgeseter PM10 µg/m³ Day",
        "Elgeseter PM2.5 µg/m³ Day",
    ]

    for col in cols:
        df[col] = df[col].str.replace(",", ".").astype(float)
        antall_negative = (df[col] < 0).sum()
        df[col] = df[col].clip(lower=0)
        print(f"Fjernet {antall_negative} negative verdier i kolonnen '{col}'.")

    return df
