import pandas as pd
import random

# Script for å simulere feil i historiske temperaturdata

antall_år=50
df = pd.read_csv(f"data/temp_gloshaugen_historisk_{antall_år}år.csv")

#Legger til manglende verdier på 10 tilfeldige rader
indekser = random.sample(range(len(df)), 10)  
for i in indekser:
    df.at[i, 'temperatur'] = None

#Legger til outliers på 5 tilfeldige rader
outlier_indekser = random.sample(range(len(df)), 5)
for i in outlier_indekser:
    df.at[i, 'temperatur'] = random.choice([-100, 100, 999])  # urealistiske temperaturer

#Kopier noen rader og legg dem inn igjen
duplikater = df.sample(5)
df = pd.concat([df, duplikater], ignore_index=True)

#Lagrer endringen/feilene i en ny fil
df.to_csv(f"data/temp_gloshaugen_historisk_inneholder_feil_{antall_år}år.csv", index=False)
print("CSV-fil med feil er lagret")
