import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from bokeh.plotting import figure, output_notebook, show
from bokeh.models import ColumnDataSource, HoverTool, Arrow, NormalHead, Annulus, Label
from datetime import datetime
from statistikk import analyser_fil
import calendar
from statistikk import beregn_avvik, analyser_temperatur, beregn_endring_totalt
from datainnsamling_temperatur import hent_temperaturer, hent_sanntidsdata
import numpy as np

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



# Linjediagram av årlig gjennomsnittstemperatur med Bokeh
def plot_interactive_bokeh(årlig_df):

    # Gjør DataFrame om til ColumnDataSource for hover-verktøy
    src = ColumnDataSource(årlig_df)
    output_notebook()

    # Sett opp figur
    p = figure(
        title="Årlig gjennomsnittstemperatur på Gløshaugen",
        x_axis_label="År",
        y_axis_label="Temperatur (°C)",
        sizing_mode="stretch_width",
        height=350,
        tools="pan,wheel_zoom,box_zoom,reset"
    )

    # Legg til hover
    hover = HoverTool(tooltips=[
        ("År",             "@år"),
        ("Temperatur",     "@gjennomsnitt{0.2f} °C"),
        ("Median",         "@median{0.2f} °C")
    ])
    p.add_tools(hover)

    # Tegn linje + punkter
    p.line("år", "gjennomsnitt", source=src, line_width=2)
    p.scatter("år", "gjennomsnitt", source=src, size=6, fill_color="white", marker="circle")

    # Finn varmeste og kaldeste
    varm = årlig_df.loc[årlig_df["gjennomsnitt"].idxmax()]
    kald = årlig_df.loc[årlig_df["gjennomsnitt"].idxmin()]
    
    # Tegner ring rundt varmeste punkt
    ring_varm = Annulus(
        x=varm["år"], y=varm["gjennomsnitt"],
        inner_radius=0.5, outer_radius=0.55,
        line_color="red", line_width=1
    )
    p.add_glyph(ring_varm)

    # Label ved varmeste
    label_varm = Label(
        x=varm["år"], y=varm["gjennomsnitt"],
        x_offset=10, y_offset=-20,
        text=f"Varmest\n{int(varm['år'])}: {varm['gjennomsnitt']:.2f}°C",
        text_color="red",
        text_font_size="9pt"
    )
    p.add_layout(label_varm)

    # Tegner ring rundt kaldeste punkt
    ring_kald = Annulus(
        x=kald["år"], y=kald["gjennomsnitt"],
        inner_radius=0.5, outer_radius=0.55,
        line_color="red", line_width=1
    )
    p.add_glyph(ring_kald)

    # Label ved kaldeste
    label_kald = Label(
        x=kald["år"], y=kald["gjennomsnitt"],
        x_offset=-65, y_offset=-20,
        text=f"Kaldest\n{int(kald['år'])}: {kald['gjennomsnitt']:.2f}°C",
        text_color="red",
        text_font_size="9pt"
    )
    p.add_layout(label_kald)

    show(p)



# Søylediagram av årlig snittemperatur per tiår
def plot_by_decade(tiårs_df):
    plt.figure(figsize=(10,5))
    ax = sns.barplot(data=tiårs_df, x="tiår", y="gjennomsnitt", color="steelblue", err_kws={"color": "none"})
    ax.set_title("Gjennomsnitt per tiår")
    ax.set_xlabel("Tiår")
    ax.set_ylabel("Temperatur (°C)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    for bar in ax.patches:
        h = bar.get_height()
        x = bar.get_x() + bar.get_width() / 2
        ax.text(x, h + 0.05, f"{h:.2f}", 
                ha="center", va="bottom", fontsize=8)
        
    plt.show()


# Heatmap av temperaturer per måned og år
def plot_temp_heatmap(df, årskolonne='år', månedskolonne='måned', verdikolonne='temperatur'):
    # Lager pivottabell der radene er måneder og kolonnene er år
    pivot = df.pivot(index=månedskolonne, columns=årskolonne, values=verdikolonne)
    # Sørger for at radene ligger i rekkefølge 1–12
    pivot = pivot.reindex(range(1, 13))
    
    # Plotter
    plt.figure(figsize=(14, 4))
    sns.heatmap(
        pivot,
        cmap='coolwarm',        # rød-blå fargekart
        cbar_kws={'label': verdikolonne},
        linewidths=0.5,         # streker mellom rutene
        annot=False,             # vis tallene i rutene
        #fmt=".1f",              # én desimal
        linecolor='white' 
    )
    # Label aksene med månednavn
    plt.title("Gjennomsnittstemperatur per måned og år")
    plt.xlabel("År")
    plt.ylabel("Måned")
    plt.yticks(
        ticks=range(0,12),
        labels=['Jan','Feb','Mar','Apr','Mai','Jun','Jul','Aug','Sep','Okt','Nov','Des'],
        rotation=0
    )
def plot_temperatur_år(df):
    plt.figure(figsize=(10, 5))
    plt.plot(df["år"], df["gjennomsnitt"], marker="o")
    plt.title("Årlig gjennomsnittstemperatur")
    plt.xlabel("År")
    plt.ylabel("Temperatur (°C)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_avvik(df):
    df_avvik = beregn_avvik(df, verdikolonne="gjennomsnitt")
    
    plt.figure(figsize=(12, 5))
    sns.barplot(data=df_avvik, x="år", y="avvik", hue="år", palette="coolwarm", dodge=False, legend=False)

    plt.axhline(0, color="black", linewidth=1)
    plt.title("Årlig temperaturavvik fra totalgjennomsnitt")
    plt.xlabel("År")
    plt.ylabel("Avvik (°C)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def tegn_endring_sol(filsti):

    resultat = analyser_temperatur(filsti)
    df_temp = resultat["temperatur"]["årlig_snitt"]
    endring = beregn_endring_totalt(df_temp)

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_aspect("equal")
    ax.axis("off")

    # Solsirkel
    sol = plt.Circle((0.5, 0.5), 0.3, color="yellow", ec="orange", lw=4)
    ax.add_patch(sol)

    # Tekst i sol
    tekst = f"+{endring['endring']:.2f}°C)"
    ax.text(0.5, 0.5, tekst, ha="center", va="center", fontsize=14, fontweight="bold", color="black")

    n_stråler = 12
    for i in range(n_stråler):
        vinkel = 2 * np.pi * i / n_stråler
        x0, y0 = 0.5 + 0.31 * np.cos(vinkel), 0.5 + 0.31 * np.sin(vinkel)
        x1, y1 = 0.5 + 0.42 * np.cos(vinkel), 0.5 + 0.42 * np.sin(vinkel)
        ax.plot([x0, x1], [y0, y1], color="orange", lw=2)

    plt.title(f"Temperaturøkning fra {endring['startår']} til {endring['sluttår']}", pad=20)
    plt.show()




def plot_sanntids_temperatur(lat=63.4195, lon=10.4065):
    data = hent_sanntidsdata(lat, lon)
    if not data:
        print("Klarte ikke hente sanntidsdata.")
        return
    temperaturer = hent_temperaturer(data)
    if not temperaturer:
        print("Ingen temperaturer funnet.")
        return

    df = pd.DataFrame(temperaturer, columns=["tid", "temperatur"])
    df["tid"] = pd.to_datetime(df["tid"])

    plt.figure(figsize=(10, 5))
    plt.plot(df["tid"], df["temperatur"], marker="o")
    plt.title("Sanntidstemperatur (Værvarsel for kommende dager)")
    plt.xlabel("Tid")
    plt.ylabel("Temperatur (°C)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


    # Heatmap av månedlig temperatur over flere år
from temp_visualisering import plot_temp_heatmap

# Leser inn og aggregér til månedsgjennomsnitt
stat_dict, _, _ = analyser_fil(
    filsti="../data/temp_gloshaugen_historisk_renset_ 50.csv",
    sep=",",
    datokolonne="tidspunkt",
    groupby="måned"
)
måned_df = stat_dict["temperatur"] 
# Fjerner 2025 siden det er ufullstendig
måned_df = måned_df[måned_df["år"] < 2025]

plot_temp_heatmap(
    måned_df,
    årskolonne="år",
    månedskolonne="måned",
    verdikolonne='gjennomsnitt'
)
