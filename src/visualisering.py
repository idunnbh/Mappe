import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datainnsamling_luftkvalitet import df_selected



# Konverterer til Pandas datetime-objekter og sorterer kronologisk
df_selected["from"] = pd.to_datetime(df_selected["from"])
df_selected = df_selected.sort_values("from")

# Plotter linjediagram for luftkvalitetsvarsel
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_selected, x="from", y="variables.pm10_concentration.value", label="PM10")
sns.lineplot(data=df_selected, x="from", y="variables.pm25_concentration.value", label="PM2.5")
sns.lineplot(data=df_selected, x="from", y="variables.no2_concentration.value", label="NO₂")
plt.xlabel("Tid")
plt.ylabel("Konsentrasjon (µg/m³)")
plt.title("Luftkvalitetsvarsel")
plt.xticks(rotation=45)
plt.show()