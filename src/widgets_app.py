
import ipywidgets as widgets
from IPython.display import display
from statistikk import analyser_fil
from temp_visualisering import load_and_compute

from dotenv import load_dotenv
load_dotenv("../api.env")

import os, sys
sys.path.append(os.path.abspath("../src"))

# Henter data
statistikk_norge, df_total_norge, df_norge_alt = analyser_fil("../data/klimagassutslipp_norge_renset.csv", datokolonne="år", groupby="år")
statistikk_verden, df_total_verden, df_verden_alt = analyser_fil("../data/klimagassutslipp_verden_renset.csv", datokolonne="År", groupby="år")


df_norge = df_total_norge[df_total_norge["kilde_(aktivitet)"].str.lower().str.contains("alle kilder")].copy()
df_norge = df_norge[["år", "utslipp_til_luft_(1_000_tonn_co2-ekvivalenter,_ar5)"]]
df_norge.rename(columns={"utslipp_til_luft_(1_000_tonn_co2-ekvivalenter,_ar5)": "gjennomsnitt"}, inplace=True)
df_norge_alt = df_norge_alt.rename(columns={"utslipp_til_luft_(1_000_tonn_co2-ekvivalenter,_ar5)": "gjennomsnitt"})
df_verden = df_verden_alt.rename(columns={"utslipp_i_co2_ekvivalenter": "gjennomsnitt"})

temp_fil = "../data/temp_gloshaugen_historisk_renset_ 50.csv"
klima_fil = "../data/klimagassutslipp_verden_renset.csv"
luft_fil = "../data/gyldig_historisk_luftkvalitet.csv"

årlig_temp_df, tiårs_temp_df = load_and_compute(temp_fil)


from statistikk import analyser_luftkvalitet, legg_til_tid
_, _, df_luft = analyser_fil(luft_fil, datokolonne="tid", groupby="år")
df_luft = legg_til_tid(df_luft)
målinger = [kol for kol in df_luft.columns if "ugm3" in kol]
luftdata = analyser_luftkvalitet(df_luft, målinger)

# Widgets
valg = widgets.ToggleButtons(
    options=["Temperaturdata", "Klimagassutslipp", "Luftkvalitet", "Prediktiv visualisering"],
    description='Analyser:', button_style='info'
)
sted_widget = widgets.Dropdown(
    options=['Trykk her for å velge', 'Norge', 'Globalt', 'Sammenlign'],
    value='Trykk her for å velge', description='Sted:'
)

datatype_widget = widgets.Dropdown(
    options=["Trykk her for å velge", "Historiske data", "Sanntidsdata"],
    value="Trykk her for å velge", description="Datakilde:"
)

år_widget = widgets.IntSlider(
    description="Velg år:",
    min=df_norge_alt["år"].min(),
    max=df_norge_alt["år"].max(),
    value=df_norge_alt["år"].min(),
    continuous_update=False )

temp_plott_valg = widgets.Dropdown(
    options=["Trykk her for å velge", "Årlig utvikling", "Gjennomsnitt per tiår", "Avvik fra snitt", "Endring total (SOL)"],
    value="Trykk her for å velge", description="Temperatur:" )

sanntid_plott_valg = widgets.Dropdown(
    options=["Trykk her for å velge", "Temperatur neste dager"],
    value="Trykk her for å velge",
      description="Plott:")

lufttype_plott_valg = widgets.Dropdown(
    options=["NO₂", "PM10", "PM2.5"],
    value="NO₂",
    description="Komponent:")

luft_plott_valg = widgets.Dropdown(
    options=["Årsgjennomsnitt", "Månedsnitt"],
    value= "Årsgjennomsnitt",
    description="Periode:"
)

prediktiv_plott_valg = widgets.Dropdown(
    options=[
        "Trykk her for å velge",
        "Temperatur vs CO₂-utslipp",
        "Temperatur vs Luftkvalitet (NO₂)",
        "Temperatur vs Luftkvalitet (PM10)",
        "Temperatur vs Luftkvalitet (PM2.5)"],
    value="Trykk her for å velge", description="Plott:")

klima_plott_valg = widgets.Dropdown(description="Velg plott:")
ny_graf_knapp = widgets.Button(description="Se ny graf", button_style='warning')
output = widgets.Output()


def setup_widgets():
    display(valg)
    display(output)

# Eksporter alle relevante variabler
__all__ = [
    "valg", "sted_widget", "datatype_widget", "år_widget", "temp_plott_valg",
    "sanntid_plott_valg", "lufttype_plott_valg", "prediktiv_plott_valg", "klima_plott_valg",
    "ny_graf_knapp", "output", "setup_widgets",
    "df_norge", "df_norge_alt", "df_verden", "årlig_temp_df", "tiårs_temp_df",
    "temp_fil", "klima_fil", "luft_fil", "luftdata"
]
