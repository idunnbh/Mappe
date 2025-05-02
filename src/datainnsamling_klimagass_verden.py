import pandas as pd
import os

os.makedirs("data", exist_ok=True)

data_url = "https://ourworldindata.org/grapher/total-ghg-emissions.csv?v=1&csvType=filtered&useColumnShortNames=false&tab=chart&time=1973..latest&country=~OWID_WRL"

print("Henter data fra Our World in Data...")
df = pd.read_csv(data_url, storage_options={'User-Agent': 'OWID-fetch'})

csv_path = "data/klimagassutslipp_verden.csv"
df.to_csv(csv_path, index=False)
print(f"Data lagret til {csv_path}")
