import sys
import os

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from IPython.display import display, HTML

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

    try:
        df = hent_sanntids_luftkvalitet()
        if df is None or df.empty:
            raise ValueError("Ingen data hentet!")
        
        df["from"] = pd.to_datetime(df["from"])
        df.set_index("from", inplace=True)

        max_no2 = df["variables.no2_concentration.value"].max()
        max_pm10 = df["variables.pm10_concentration.value"].max()
        max_pm25 = df["variables.pm25_concentration.value"].max()

        varsler = []

        if max_no2 > 200:
            tidspunkt_no2 = df["variables.no2_concentration.value"].idxmax()
            dato_no2 = tidspunkt_no2.date()
            varsler.append(f"Det kan bli høye NO₂-nivåer ({max_no2:.0f} µg/m³) den {dato_no2}. Ikke vær for mye ute.")

        if max_pm10 > 50:
            tidspunkt_pm10 = df["variables.pm10_concentration.value"].idxmax()
            dato_pm10 = tidspunkt_pm10.date()
            varsler.append(f"Det kan bli høye PM10-nivåer ({max_pm10:.0f} µg/m³) den {dato_pm10}. Hold deg inne! Dette kan påvirke luftveiene.")

        if max_pm25 > 25:
            tidspunkt_pm25 = df["variables.pm25_concentration.value"].idxmax()
            dato_pm25 = tidspunkt_pm25.date()
            varsler.append(f" Det kan bli høy PM2.5-nivåer ({max_pm25:.0f} µg/m³) den {dato_pm25}. Dette er over anbefalt grense og er spesielt farlig for barn og eldre.")
        
        if varsler:
            melding = "<b>Varsel om dårlig luftkvalitet:</b><br>" + "<br>".join(varsler)
            display(HTML(f"""
                <div style='
                border: 1px solid red;
                padding: 10px;
                margin-bottom: 10px;
                font-size: 15px;
            '>{melding}</div>
        """))

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

    except Exception as e:
        display(HTML("""
        <div style='color:red; font-size:18px; font-weight:bold;'>
        Klarte ikke hente sanntidsdata. Har du lagt inn API-nøkkel? </div>
        <div style='color:gray; font-size:16px;'>Viser demo-data i stedet:)</div>
        """))
        plot_demo_luftkvalitet()


def plot_demo_luftkvalitet(filnavn="../data/luftkvalitet_sanntid_demo.csv"):
    try:
        display(HTML("<span style='color:red; font-size:18px; font-weight:bold;'>Dette er kun en demo! Dette gjør at du kan bruke appen også hvis du ikke har API-nøkkel</span>"))
        
        df = pd.read_csv(filnavn)
        df["from"] = pd.to_datetime(df["from"])
        df.set_index("from", inplace=True)

        max_no2 = df["variables.no2_concentration.value"].max()
        max_pm10 = df["variables.pm10_concentration.value"].max()
        max_pm25 = df["variables.pm25_concentration.value"].max()

        varsler = []

        if max_no2 > 200:
            tidspunkt_no2 = df["variables.no2_concentration.value"].idxmax()
            dato_no2 = tidspunkt_no2.date()
            varsler.append(f"Det kan bli høye NO₂-nivåer ({max_no2:.0f} µg/m³) den {dato_no2}! Ikke vær for mye ute.")

        if max_pm10 > 50:
            tidspunkt_pm10 = df["variables.pm10_concentration.value"].idxmax()
            dato_pm10 = tidspunkt_pm10.date()
            varsler.append(f"Det kan bli høye PM10-nivåer ({max_pm10:.0f} µg/m³) den {dato_pm10}! Hold deg inne! Dette kan påvirke luftveiene.")

        if max_pm25 > 25:
            tidspunkt_pm25 = df["variables.pm25_concentration.value"].idxmax()
            dato_pm25 = tidspunkt_pm25.date()
            varsler.append(f" Det kan bli høy PM2.5-nivåer ({max_pm25:.0f} µg/m³) den {dato_pm25}. Dette er over anbefalt grense og er spesielt farlig for barn og eldre.")
        
        if varsler:
            melding = "<b>Varsel om dårlig luftkvalitet:</b><br>" + "<br>".join(varsler)
            display(HTML(f"""
                <div style='
                border: 1px solid red;
                padding: 10px;
                margin-bottom: 10px;
                font-size: 15px;
            '>{melding}</div>
        """))


        plt.figure(figsize=(10, 6))
        plt.plot(df.index, df["variables.no2_concentration.value"], label="NO2")
        plt.plot(df.index, df["variables.pm10_concentration.value"], label="PM10")
        plt.plot(df.index, df["variables.pm25_concentration.value"], label="PM2.5")
        plt.title("Luftkvalitet (demo-data)")
        plt.xlabel("Tid")
        plt.ylabel("µg/m³")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Feil ved lesing av demo-data: {e}")

