import pandas as pd
import random

df = pd.read_csv("data/temp_gloshaugen_historisk.csv")

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
df.to_csv("data/temp_gloshaugen_historisk_inneholder_feil.csv", index=False)
print("CSV-fil med feil er lagret")
