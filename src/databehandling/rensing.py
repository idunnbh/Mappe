import pandas as pd

def last_in_csv(filsti):
    return pd.read_csv(filsti)

def håndter_manglende_verdier(df):
    if df.isnull().values.any():
        print("Manglende verdier funnet->fyller med gjennomsnitt.")
    df['temperatur'] = df['temperatur'].fillna(df['temperatur'].mean())
    return df

def fjern_duplikater(df):
    før = len(df)
    df = df.drop_duplicates()
    etter = len(df)
    print(f"Fjernet {før - etter} duplikater.")
    return df

def fjern_outliers(df, min_temp=-50, max_temp=50):
    før = len(df)
    df = df[(df['temperatur'] >= min_temp) & (df['temperatur'] <= max_temp)]
    etter = len(df)
    print(f"Fjernet {før - etter} outliers.")
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
    df = fjern_duplikater(df)
    return df