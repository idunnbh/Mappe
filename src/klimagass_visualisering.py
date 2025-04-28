import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys, os

sys.path.append(os.path.abspath("../src"))

from statistikk import tiår_snitt

# Lager linjediagram som viser utviklingen i utslipp per år
def plot_utslipp(df, datokolonne="år", verdi_kolonne="gjennomsnitt", tittel="Utslipp per år", ax=None, fig=None, farge="pink"): 
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 5))  # Nå lager vi både fig og ax
    sns.lineplot(data=df, x=datokolonne, y=verdi_kolonne, marker="o", ax=ax, color=farge)
    ax.set_title(tittel)
    ax.set_xlabel("År")
    ax.set_ylabel("Utslipp (CO₂-ekvivalenter)")
    ax.tick_params(axis="x", rotation=45)
    if fig is not None:  # Bare vis hvis vi laget figuren selv
        plt.tight_layout()
        plt.show()


# Lager et stolpediagram som viser gjennomsnittlig utslipp per tiår
def plot_utslipp_per_tiar(df, tittel="Gjennomsnittlig utslipp per tiår"):
    tiårssnitt_df = tiår_snitt(df)
    plt.figure(figsize=(7, 4))
    sns.barplot(data=tiårssnitt_df, x="tiår", y="gjennomsnitt")
    plt.title(tittel)
    plt.xlabel("Tiår")
    plt.ylabel("Utslipp (CO₂-ekvivalenter)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Plotter utslipp i Norge og verden i samme graf med to y-akser
def plot_norge_og_verden_sammen(df_norge, df_verden, verdi_kolonne_norge="gjennomsnitt", verdi_kolonne_verden="gjennomsnitt"):
    fig, ax1 = plt.subplots(figsize=(10, 4))

    plot_utslipp(df_norge, ax=ax1, farge="purple", tittel=None)
    ax2 = ax1.twinx()
    plot_utslipp(df_verden, ax=ax2, farge="orange", tittel=None)

    plt.title("Klimagassutslipp: Norge vs Verden")
    fig.tight_layout()
    plt.show()

# Plotter utslipp i Norge og verden i to separate grafer
def plot_norge_og_verden_separat(df_norge, df_verden):

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    plot_utslipp(df_norge, ax=ax1, farge="purple", tittel="Klimagassutslipp i Norge")
    plot_utslipp(df_verden, ax=ax2, farge="orange", tittel="Klimagassutslipp i verden")

    plt.suptitle("Klimagassutslipp: Norge og Verden", fontsize=16)
    plt.tight_layout()
    plt.show()

# Lager et linjediagram som viser utslipp per kilde over tid
def plot_utslipp_per_kilde(df, datokolonne="år", gruppering="kilde_(aktivitet)", verdi_kolonne="gjennomsnitt"):
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x=datokolonne, y=verdi_kolonne, hue=gruppering, marker="o")
    plt.title("Klimagassutslipp per kilde")
    plt.xlabel("År")
    plt.ylabel("Utslipp (CO₂-ekvivalenter)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend(title="Kilde")
    plt.show()


# Lager et kakediagram som viser andel utslipp per kilde for valgt år
def plot_andel_per_kilde(df, år, årskolonne='år', kildekolonne='kilde_(aktivitet)', utslippkolonne='gjennomsnitt'):

    df = df.copy()
    df_år = df[df[årskolonne] == år]

    if df_år.empty:
        print(f"Ingen data for året {år}.")
        return

    plt.figure(figsize=(6, 6))
    plt.pie(df_år[utslippkolonne], labels=df_år[kildekolonne], autopct='%1.1f%%', startangle=90, counterclock=False)
    plt.title(f"Andel av utslipp per kilde i {år}")
    plt.axis('equal') 
    plt.show()

# Lager et heatmap som viser utslipp per kilde og år
def plot_heatmap_per_kilde(df):
    heatmap_data = df.pivot(index="kilde_(aktivitet)", columns="år", values="gjennomsnitt")
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, cmap="YlOrRd", linewidths=0.5, linecolor='white')
    
    plt.title("Klimagassutslipp per kilde og år (heatmap)", fontsize=16)
    plt.xlabel("År")
    plt.ylabel("Kilde")
    plt.tight_layout()
    plt.show()
