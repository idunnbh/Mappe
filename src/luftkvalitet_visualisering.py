import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from datainnsamling_luftkvalitet import df_valid

import dataanalyse
import importlib
importlib.reload(dataanalyse)


 
df_hist = df_valid.copy()

# Konverterer til Pandas datetime-objekter og sorterer kronologisk
df_hist['Tid'] = pd.to_datetime(
    df_hist['Tid'],
    dayfirst=True,                # datoformatet er DD.MM.YYYY
    format='%d.%m.%Y %H:%M'
)
df_hist = df_hist.sort_values("Tid")

# Plotter linjediagram for historisk luftkvalitet
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_hist, x="Tid", y="Elgeseter PM10 µg/m³ Day", label="PM10")
sns.lineplot(data=df_hist, x="Tid", y="Elgeseter PM2.5 µg/m³ Day", label="PM2.5")
sns.lineplot(data=df_hist, x="Tid", y="Elgeseter NO2 µg/m³ Day", label="NO₂")
plt.xlabel("Tid")
plt.ylabel("Konsentrasjon (µg/m³)")
plt.title("Luftkvalitet siste 20 år")
plt.xticks(rotation=45)
#plt.show()


