import pandas as pd 

   # Fjerner "" fra navnene og renser kolonnene
def rens_kolonnenavn_klimagass(df):
    df.columns = df.columns.str.replace('"', '')
    return df

    # Fjerner duplikater
def duplikater_klimagass(df):
    før = len(df)
    df = df.drop_duplicates()
    etter = len(df)
    print(f"Fjernet {før - etter} duplikater.")
    return df

def rens_klimagass(df):
    df = rens_kolonnenavn_klimagass(df)
    df = duplikater_klimagass(df)
    print("Databehandling fullført. \n")
    return df