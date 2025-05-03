import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

 
import matplotlib.pyplot as plt

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

def plott_endring_over_tid(df, stoff):
    df["endring"] = df["årsgjennomsnitt"].diff()
    plt.figure(figsize=(8, 4))
    plt.plot(df["år"], df["årsgjennomsnitt"], label="Snitt")
    plt.plot(df["år"], df["endring"], label="Årlig endring", linestyle="--")
    plt.title(f"Endringer i årssnitt for {stoff}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

