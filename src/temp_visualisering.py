import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from bokeh.plotting import figure, output_notebook, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.models import Arrow, NormalHead, Annulus
from datetime import datetime

# Aktiver inline-visning i Jupyter
output_notebook()


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
def plot_interactive_bokeh(annual_df):
    # Gjør DataFrame om til ColumnDataSource for hover-verktøy
    src = ColumnDataSource(annual_df)

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
        ("År", "@år"),
        ("Temp", "@gjennomsnitt{0.2f} °C"),
    ])
    p.add_tools(hover)

    # Tegn linje + punkter
    p.line("år", "gjennomsnitt", source=src, line_width=2)
    p.circle("år", "gjennomsnitt", source=src, size=6, fill_color="white")
    
    # Tegner ring rundt varmeste punkt
    ann = Annulus(
        x=2020, y=8.76,
        inner_radius=0.69, outer_radius=0.7,
        line_color="red", line_width=1 
    )
    p.add_glyph(ann)

    # Tegner ring rundt kaldeste punkt
    ann = Annulus(
        x=1985, y=4.67,
        inner_radius=0.69, outer_radius=0.7,
        line_color="red", line_width=1
    )
    p.add_glyph(ann)

    show(p)

# Søylediagram av årlig snittemperatur per tiår
def plot_by_decade(decade_df):
    plt.figure(figsize=(10,5))
    sns.barplot(data=decade_df, x="tiår", y="gjennomsnitt", palette="Blues_d")
    plt.title("Gjennomsnitt per tiår")
    plt.xlabel("Tiår"); plt.ylabel("Temperatur (°C)")
    plt.xticks(rotation=45); plt.tight_layout()
    plt.show()



