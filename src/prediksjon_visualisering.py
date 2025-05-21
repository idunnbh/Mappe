import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression

from statistikk import analyser_temperatur, analyser_fil, legg_til_tid


# Kobler temperaturdata og CO₂-utslippsdata basert på år
def last_og_koble_data(temp_fil, klima_fil):
    temp_resultat = analyser_temperatur(temp_fil, datokolonne="tidspunkt", groupby="måned")
    temp_df = temp_resultat["temperatur"]["årlig_snitt"]


    resultat, _, _ = analyser_fil(klima_fil, datokolonne="År", groupby="år")
    klima_agg = resultat["utslipp_i_co2_ekvivalenter"]

    df_merged = pd.merge(temp_df, klima_agg, on="år", how="inner")
    return df_merged

# Plotter temperatur og CO₂-utslipp over tid
def plot_temp_vs_klima(df_merged):
    plt.figure(figsize=(8, 5))
    plt.plot(df_merged["år"], df_merged["årsgjennomsnitt"], label="Temperatur (°C)")
    plt.plot(df_merged["år"], df_merged["gjennomsnitt"] / 1e10, label="CO2-utslipp (×10⁹ tonn)")
    plt.xlabel("År")
    plt.ylabel("Verdi")
    plt.title("Utvikling i temperatur og CO2-utslipp over tid")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Lager et scatter-plot mellom temperatur og CO₂-utslipp
def scatter_temp_vs_utslipp(df, x_col="gjennomsnitt", y_col="årsgjennomsnitt"):
    plt.figure(figsize=(7, 5))
    sns.scatterplot(
        data=df,
        x=x_col,
        y=y_col,
        alpha=0.7,
        s=60,
        color="rebeccapurple"
    )
    plt.title("Temperatur i Norge vs. globale CO₂-utslipp")
    plt.xlabel("Globale CO₂-utslipp (tonn)")
    plt.ylabel("Årsgjennomsnitt temperatur")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# Lager regresjonsplott mellom temperatur og CO₂-utslipp 
def plot_regresjon_temp_vs_utslipp(df, x_col="gjennomsnitt", y_col="årsgjennomsnitt"):

    plt.figure(figsize=(7, 5))
    sns.regplot(
        data=df,
        x=x_col,
        y=y_col,
        scatter=True,
        ci=95,
        line_kws={"color": "orangered", "linewidth": 2},
        color="rebeccapurple"
    )
    plt.title("Temperatur i Norge vs. globale CO₂-utslipp (med regresjonslinje)")
    plt.xlabel("Globale CO₂-utslipp (tonn)")
    plt.ylabel("Årsgjennomsnitt temperatur")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Kobler sammen temperaturdata og luftkvalitetsdata 
def last_og_koble_temp_luft(temp_fil, luft_fil, stoffnavn):

    temp_resultat = analyser_temperatur(temp_fil, datokolonne="tidspunkt", groupby="måned")
    temp_df = temp_resultat["temperatur"]["årlig_snitt"]

    df_luft = pd.read_csv(luft_fil)
    df_luft = legg_til_tid(df_luft, tidkolonne="Tid", groupby="år")
    
    if stoffnavn not in df_luft.columns:
        print(f"Fant ikke '{stoffnavn}' i luftdata.")
        return None
    
    df_luft_aarlig = df_luft.groupby("år")[stoffnavn].mean().reset_index()

    df_merged = pd.merge(temp_df, df_luft_aarlig, on="år", how="inner")
    return df_merged

# Plotter regresjon mellom temperatur og konsentrasjonen av valgt luftforurensningsstoff
def plot_regresjon_luftkvalitet_vs_temp(df_merged, stoff="no2"):
    if stoff not in df_merged.columns:
        print(f"Fant ikke '{stoff}' i datasettet.")
        return

    plt.figure(figsize=(7, 5))
    sns.regplot(
        data=df_merged,
        x="årsgjennomsnitt", y=stoff,
        scatter=True,
        color="seagreen",
        line_kws={"color": "darkred", "linewidth": 2}
    )

    plt.title(f"Sammenheng mellom temperatur og {stoff}-nivå")
    plt.xlabel("Årsgjennomsnitt temperatur (°C)")
    plt.ylabel(f"{stoff}-konsentrasjon (µg/m³)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
