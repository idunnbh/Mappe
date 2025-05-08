
import ipywidgets as widgets
from IPython.display import display, clear_output

import sys, os
sys.path.append(os.path.abspath("../src"))


from widgets_app import (
    valg, sted_widget, datatype_widget, år_widget, temp_plott_valg,
    temp_sanntid_plott_valg, lufttype_plott_valg, luft_plott_valg, prediktiv_plott_valg,
    klima_plott_valg, ny_graf_knapp, output,
    df_norge, df_norge_alt, df_verden,
    årlig_temp_df, temp_fil, klima_fil, luft_fil, luftdata, luft_sanntid_plott_valg
)


from klimagass_visualisering import *
from temp_visualisering import *
from prediksjon_visualisering import *
from luftkvalitet_visualisering import *
from statistikk import tiår_snitt


def vis_valgt_data(endring):
    output.clear_output()
    if valg.value == "Klimagassutslipp":
        with output:
            display(widgets.HTML("<h4>Analyse av klimagassutslipp </h4>"))   
            display(sted_widget)
            oppdater_plottvalg()
            display(klima_plott_valg)
    elif valg.value == "Temperaturdata":
        with output:
            display(widgets.HTML("<h4>Analyse av temperaturdata på Gløshaugen</h4>"))    
            display(datatype_widget)
            if datatype_widget.value == "Historiske data":
                display(temp_plott_valg)
            elif datatype_widget.value == "Sanntidsdata":
                display(temp_sanntid_plott_valg)
    elif valg.value == "Luftkvalitet":
        with output:
            display(widgets.HTML("<h4>Analyse av luftkvalitet på Elgseter</h4>"))  
            display(datatype_widget)
            if datatype_widget.value == "Historiske data":
                display(lufttype_plott_valg)
                display(luft_plott_valg)
            elif datatype_widget.value == "Sanntidsdata":
                display(luft_sanntid_plott_valg)
    elif valg.value == "Prediktiv visualisering":
        with output:
            display(widgets.HTML("<h4>Velg analyse for prediktiv visualisering</h4>"))
            display(prediktiv_plott_valg) 

           

def vis_klimagass_plot(endring):
    if endring['name'] == 'value':
        output.clear_output(wait=True)
        with output:
            if klima_plott_valg.value == "Utslipp per år":
                df = df_norge if sted_widget.value == "Norge" else df_verden
                plot_utslipp(df, tittel=f"Årlige utslipp i {sted_widget.value}")

            elif klima_plott_valg.value == "Utslipp per tiår":
                df = df_norge if sted_widget.value == "Norge" else df_verden
                plot_utslipp_per_tiar(df)

            elif klima_plott_valg.value == "Utslipp per kilde (linjeplot)":
                plot_utslipp_per_kilde(df_norge_alt)

            elif klima_plott_valg.value == "Utslipp per kilde (kakediagram for et år)":
                år_widget.value = år_widget.min
                display(år_widget)
                år_widget.observe(vis_kake_plot, names='value')

                plot_andel_per_kilde(df_norge_alt, år_widget.value)
                
            elif klima_plott_valg.value == "Heatmap per kilde":
                plot_heatmap_per_kilde(df_norge_alt)

            elif klima_plott_valg.value == "Samme graf":
                plot_norge_og_verden_sammen(df_norge, df_verden)

            elif klima_plott_valg.value == "Separate grafer":
                plot_norge_og_verden_separat(df_norge, df_verden)

            display(ny_graf_knapp)

def vis_kake_plot(e):
    if e['name'] == 'value':
        output.clear_output(wait=True)
        with output:
            display(år_widget)
            plot_andel_per_kilde(df_norge_alt, år_widget.value)
            display(ny_graf_knapp)

def oppdater_plottvalg(endring=None):
    if sted_widget.value == "Norge":
        klima_plott_valg.options = [
            "Utslipp per år", "Utslipp per tiår", "Utslipp per kilde (linjeplot)",
            "Utslipp per kilde (kakediagram for et år)", "Heatmap per kilde"
        ]
    elif sted_widget.value == "Globalt":
        klima_plott_valg.options = ["Utslipp per år", "Utslipp per tiår"]
    elif sted_widget.value == "Sammenlign":
        klima_plott_valg.options = ["Samme graf", "Separate grafer"]


def vis_temperatur_plot(endring):
    output.clear_output(wait=True)

    with output:
        if datatype_widget.value == "Historiske data":
            valgt_plott = temp_plott_valg.value
            if valgt_plott == "Årlig utvikling":
                plot_temperatur_år(årlig_temp_df)
            elif valgt_plott == "Gjennomsnitt per tiår":
                tiår_df = tiår_snitt(årlig_temp_df)
                plot_by_decade(tiår_df)
            elif valgt_plott == "Avvik fra snitt":
                plot_avvik(årlig_temp_df)
            elif valgt_plott == "Endring total (SOL)" and temp_fil:
                if not os.path.exists(temp_fil):
                    print("Fant ikke temperaturfil.")
                    return
                tegn_endring_sol(temp_fil)

        elif datatype_widget.value == "Sanntidsdata":
            plot_sanntids_temperatur()

        display(ny_graf_knapp)

        
def vis_luft_plot(endring=None):
    output.clear_output(wait=True)
    with output:
    
        stoff_mapping = {
            "NO₂": "elgeseter_no2_ugm3_day",
            "PM10": "elgeseter_pm10_ugm3_day",
            "PM2.5": "elgeseter_pm2.5_ugm3_day"
        }
        stoff_valg = lufttype_plott_valg.value

        stoff = stoff_mapping[stoff_valg]
        if datatype_widget.value == "Historiske data":
            if luft_plott_valg.value == "Årsgjennomsnitt":
                plott_årssnitt(luftdata[stoff]["årlig"], stoff)
            elif luft_plott_valg.value == "Månedsnitt":
                plott_månedsnitt(luftdata[stoff]["månedlig"], stoff)

        elif datatype_widget.value == "Sanntidsdata":
            if luft_sanntid_plott_valg.value == "Sanntid søylediagram":
                plot_sanntids_luftkvalitet()

        display(ny_graf_knapp)


def vis_prediktiv_plot(endring):
    output.clear_output(wait=True)
    with output:
        if prediktiv_plott_valg.value == "Temperatur vs CO₂-utslipp":
            df = last_og_koble_data(temp_fil, klima_fil)
            plot_regresjon_temp_vs_utslipp(df)

        elif "Luftkvalitet" in prediktiv_plott_valg.value:
            stoffer = {
                "NO₂": "Elgeseter NO2 µg/m³ Day",
                "PM10": "Elgeseter PM10 µg/m³ Day",
                "PM2.5": "Elgeseter PM2.5 µg/m³ Day"
            }
            stoff = prediktiv_plott_valg.value.split(" (")[-1].replace(")", "")
            df = last_og_koble_temp_luft(temp_fil, luft_fil, stoffer[stoff])
            plot_regresjon_luftkvalitet_vs_temp(df, stoff=stoffer[stoff])
        display(ny_graf_knapp)


def tilbakestill_knapp_callback(_):
    output.clear_output()
    vis_valgt_data(None)

# Observere widgets
valg.observe(vis_valgt_data, names='value')
sted_widget.observe(oppdater_plottvalg, names='value')
klima_plott_valg.observe(vis_klimagass_plot, names='value')
datatype_widget.observe(vis_valgt_data, names='value')
temp_plott_valg.observe(vis_temperatur_plot, names='value')
temp_sanntid_plott_valg.observe(vis_temperatur_plot, names='value')
lufttype_plott_valg.observe(vis_luft_plot, names='value')
luft_plott_valg.observe(vis_luft_plot, names='value')
luft_sanntid_plott_valg.observe(vis_luft_plot, names='value')
prediktiv_plott_valg.observe(vis_prediktiv_plot, names='value')
ny_graf_knapp.on_click(tilbakestill_knapp_callback)

def kjør_app():
    display(valg)
    display(output)
    vis_valgt_data(None)
