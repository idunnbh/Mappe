import os
import json
import pandas as pd

from Datainnsamling_Idunn import process_air_quality_data

#Leser fra luftkvalitet.json
with open("data/luftkvalitet.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

df = process_air_quality_data(raw_data)

#Får ut info om dataen 
#print("\n--- DataFrame info ---")
#df.info()
    
selected_columns = [
    "from",
    "to",
    "variables.pm10_concentration.value",
    "variables.pm25_concentration.value",
    "variables.no2_concentration.value",
    "variables.o3_concentration.value",
    "variables.AQI.value",
]
df_selected = df[selected_columns]

#Får ut info om den nye dataframen 
print("\n--- Ny DataFrame info ---")
df_selected.info()



print(df_selected)