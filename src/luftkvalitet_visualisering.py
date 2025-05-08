import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

def plott_årssnitt(df, stoffnavn):
    plt.figure(figsize=(8, 5))
    plt.plot(df['år'], df['årssnitt'], marker='o')
    plt.title(f"Årsgjennomsnitt for {stoffnavn}")
    plt.xlabel("År")
    plt.ylabel("µg/m³")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plott_månedsnitt(df, stoffnavn):
    plt.figure(figsize=(8, 5))
    plt.bar(df['måned'], df['månedsnitt'])
    plt.title(f"Månedsnitt for {stoffnavn}")
    plt.xlabel("Måned")
    plt.ylabel("µg/m³")
    plt.tight_layout()
    plt.show()

def plot_sanntids_luftkvalitet():
    from datainnsamling_luft import hent_sanntids_luftkvalitet

    df = hent_sanntids_luftkvalitet()
    df["from"] = pd.to_datetime(df["from"])
    df.set_index("from", inplace=True)

    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df["variables.no2_concentration.value"], label="NO2")
    plt.plot(df.index, df["variables.pm10_concentration.value"], label="PM10")
    plt.plot(df.index, df["variables.pm25_concentration.value"], label="PM2.5")
    plt.title("Sanntids luftkvalitet")
    plt.xlabel("Tid")
    plt.ylabel("µg/m³")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
