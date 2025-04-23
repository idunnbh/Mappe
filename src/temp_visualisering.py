import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

import dataanalyse
import importlib
importlib.reload(dataanalyse)


import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))


def load_and_compute(path, datokolonne="tidspunkt"):

    # 1) Les inn og gjør datetime
    df = pd.read_csv(path)
    df[datokolonne] = pd.to_datetime(
        df[datokolonne],
        format="%Y-%m-%d %H:%M:%S%z",  # riktig rekkefølge: år-måned-dag
        utc=True
    )

    
    # 2) Årlig gjennomsnitt
    df["år"] = df[datokolonne].dt.year
    annual_df = (
        df
        .groupby("år")["temperatur"]  # bytt "verdi" med navnet på temperatur-kolonnen
        .mean()
        .reset_index(name="gjennomsnitt")
    )
    
    annual_df = annual_df.iloc[:-1]

    # 3) Tiårs-gjennomsnitt
    annual_df["tiår"] = (annual_df["år"] // 10) * 10
    decade_df = (
        annual_df
        .groupby("tiår")["gjennomsnitt"]
        .mean()
        .reset_index(name="gjennomsnitt")
    )

    return annual_df, decade_df


# Linjediagram av årlig gjennomsnittstemperatur
def plot_annual(annual_df):
    plt.figure(figsize=(10,5))
    sns.lineplot(
        data=annual_df, 
        x="år", 
        y="gjennomsnitt", 
        marker="o")
    plt.title("Årlig gjennomsnittstemperatur på Gløshaugen")
    plt.xlabel("År"); plt.ylabel("Temperatur (°C)")
    plt.xticks(rotation=45); plt.tight_layout()
    plt.show()

# Søylediagram av årlig snittemperatur per tiår
def plot_by_decade(decade_df):
    plt.figure(figsize=(10,5))
    sns.barplot(data=decade_df, x="tiår", y="gjennomsnitt", palette="Blues_d")
    plt.title("Gjennomsnitt per tiår")
    plt.xlabel("Tiår"); plt.ylabel("Temperatur (°C)")
    plt.xticks(rotation=45); plt.tight_layout()
    plt.show()



