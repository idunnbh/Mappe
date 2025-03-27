import os
import json
import pandas as pd

from Datainnsamling_Idunn import process_air_quality_data

with open("data/luftkvalitet.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

df = process_air_quality_data(raw_data)

print("\n--- DataFrame info ---")
df.info()
    
print("\n--- DataFrame describe (bare numeriske kolonner) ---")
print(df.describe())
    
print("\n--- DataFrame columns ---")
print(df.columns)
