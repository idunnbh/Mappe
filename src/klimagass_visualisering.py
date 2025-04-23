import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys, os

sys.path.append(os.path.abspath("../src"))

import dataanalyse
import importlib
importlib.reload(dataanalyse)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from dataanalyse import analyser_fil 

# Analyser og vis funksjon 
def analyser_og_vis(filsti, datokolonne="år", groupby="år", bare_total=False):
    statistikk, df_total, df = analyser_fil(filsti, datokolonne=datokolonne, groupby=groupby)

    utslipp_kol = [kol for kol in statistikk.keys() if "utslipp" in kol or "co2" in kol.lower()][0]
    df_stat = statistikk[utslipp_kol].copy()

    if bare_total and "kilde_(aktivitet)" in df_stat.columns:
        df_stat = df_stat[df_stat["kilde_(aktivitet)"].str.lower().str.contains("alle kilder")]

    df_stat["tiår"] = (df_stat["år"] // 10) * 10

    plot_utslipp_per_år(df_stat)
    plot_utslipp_per_tiår(df_stat)

# Plott av utslipp per år 
def plot_utslipp_per_år(df, datokolonne="år", verdi_kolonne="gjennomsnitt", tittel="Utslipp per år"):
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=df, x=datokolonne, y=verdi_kolonne, marker="o")
    plt.title(tittel)
    plt.xlabel("År")
    plt.ylabel("Utslipp (CO₂-ekvivalenter)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Plott uslipp per tiår 
def plot_utslipp_per_tiår(df, verdi_kolonne="gjennomsnitt"):
    snitt = df.groupby("tiår")[verdi_kolonne].mean().reset_index()
    plt.figure(figsize=(10, 5))
    sns.barplot(data=snitt, x="tiår", y=verdi_kolonne, palette="YlGnBu")
    plt.title("Gjennomsnittlig utslipp per tiår")
    plt.xlabel("Tiår")
    plt.ylabel("Utslipp (CO₂-ekvivalenter)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Samenlikner utslipp i Norge og verden 
def sammenlign_norge_og_verden_sammen(fil_norge, fil_verden):
    stat_norge, _, _ = analyser_fil(fil_norge, datokolonne="år", groupby="år")
    stat_verden, _, _ = analyser_fil(fil_verden, datokolonne="År", groupby="år")

    kol_norge = [k for k in stat_norge if "utslipp" in k.lower() or "co2" in k.lower()][0]
    kol_verden = [k for k in stat_verden if "utslipp" in k.lower() or "co2" in k.lower()][0]

    df_norge = stat_norge[kol_norge].copy()
    df_verden = stat_verden[kol_verden].copy()

    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Første akse: Norge
    color = "tab:blue"
    ax1.set_xlabel("År")
    ax1.set_ylabel("Utslipp Norge (1000 tonn CO₂)", color=color)
    ax1.plot(df_norge["år"], df_norge["gjennomsnitt"], marker="o", color=color, label="Norge")
    ax1.tick_params(axis="y", labelcolor=color)

    # Andre y-akse
    ax2 = ax1.twinx()
    color = "tab:orange"
    ax2.set_ylabel("Utslipp Verden (1000 tonn CO₂)", color=color)
    ax2.plot(df_verden["år"], df_verden["gjennomsnitt"], marker="o", color=color, label="Verden")
    ax2.tick_params(axis="y", labelcolor=color)

    plt.title("Klimagassutslipp: Norge vs Verden")
    fig.tight_layout()
    plt.show()

def sammenlign_norge_og_verden_separat(fil_norge, fil_verden):
    stat_norge, _, _ = analyser_fil(fil_norge, datokolonne="år", groupby="år")
    stat_verden, _, _ = analyser_fil(fil_verden, datokolonne="År", groupby="år")

    kol_norge = [k for k in stat_norge if "utslipp" in k.lower() or "co2" in k.lower()][0]
    kol_verden = [k for k in stat_verden if "utslipp" in k.lower() or "co2" in k.lower()][0]

    df_norge = stat_norge[kol_norge].copy()
    df_verden = stat_verden[kol_verden].copy()

    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=False)

    # Plot for Norge
    sns.lineplot(ax=axes[0], data=df_norge, x="år", y="gjennomsnitt", marker="o", color="tab:blue")
    axes[0].set_title("Norge")
    axes[0].set_xlabel("År")
    axes[0].set_ylabel("Utslipp (1 000 tonn CO₂-ekv.)")
    axes[0].tick_params(axis="x", rotation=45)

    # Plot for Verden
    sns.lineplot(ax=axes[1], data=df_verden, x="år", y="gjennomsnitt", marker="o", color="tab:orange")
    axes[1].set_title("Verden")
    axes[1].set_xlabel("År")
    axes[1].set_ylabel("Utslipp (1 000 tonn CO₂-ekv.)")
    axes[1].tick_params(axis="x", rotation=45)

    plt.suptitle("Klimagassutslipp: Norge og Verden", fontsize=14)
    plt.tight_layout()
    plt.show()

statistikk, df_total, df = dataanalyse.analyser_fil("../data/klimagassutslipp_norge_renset.csv",sep=",",datokolonne="år",groupby="år")

def plott_utslipp_per_kilde_over_tid(stats_per_kilde_år, verdi_kolonne="mean"):

    unike_kilder = stats_per_kilde_år["kilde_(aktivitet)"].unique()

    plt.figure(figsize=(12, 6))
    for kilde in unike_kilder:
        df_kilde = stats_per_kilde_år[stats_per_kilde_år["kilde_(aktivitet)"] == kilde]
        sns.lineplot(data=df_kilde, x="år", y=verdi_kolonne, label=kilde, marker="o")

    plt.title(f"Klimagassutslipp per kilde ({verdi_kolonne})")
    plt.xlabel("År")
    plt.ylabel("Utslipp (CO₂-ekvivalenter)")
    plt.xticks(rotation=45)
    plt.legend(title="Kilde")
    plt.tight_layout()
    plt.show()
