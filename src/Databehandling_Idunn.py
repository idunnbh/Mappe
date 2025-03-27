import os
import json
import pandas as pd

from Datainnsamling_Idunn import process_air_quality_data

#Leser fra luftkvalitet.json
with open("data/luftkvalitet.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

df = process_air_quality_data(raw_data)

#Får ut info om dataen 
print("\n--- DataFrame info ---")
df.info()
    
