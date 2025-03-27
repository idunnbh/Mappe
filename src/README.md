
### Rensing av temperaturdata
Det er laget en datastruktur for å rense temperaturmålinger som blir hentet  hentet fra YR.
Funksjonene som gjør dette ligger i rensing_temperaturdata.py, og disse er samlet i funksjonen rens_data(). 
Scriptet run_rensing.py kjører hele prosessen.

Dataen blir renset ved hjelp av følgende steg:
-Fjerning av duplikater
-Erstatning av manglende verdier med gjennomsnitt (fillna)
-Fjerning av outliers (temperatur < -50°C eller > 50°C)
-Automatisk lagring i data/temperatur_renset.csv
