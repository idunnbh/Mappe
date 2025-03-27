
### Rensing av temperaturdata
Det er laget en datastruktur for å rense temperaturmålinger som blir hentet  hentet fra YR.
Funksjonene som gjør dette ligger i rensing_temperaturdata.py, og disse er samlet i funksjonen rens_data(). 
Scriptet run_rensing.py kjører hele prosessen.

Dataen blir renset ved hjelp av følgende steg:
-Fjerning av duplikater
-Erstatning av manglende verdier med gjennomsnitt (fillna)
-Fjerning av outliers (temperatur < -50°C eller > 50°C)
-Automatisk lagring i data/temperatur_renset.csv

### Klimagassutslipp
Datasettet som brukes er hentet fra Statistisk sentralbyrå (https://www.ssb.no/statbank/table/13931) og inneholder data om klimagassutslipp i Norge fra 1990 til 2023. Rådataen ble hentet ut i CSV-fil og hadde små utfordringer knyttet til struktur og format. Filen inneholdt både metadata, kolonnenavn og data i samme fil.

Funksjonene for rensing ligger i rensing_temperaturdata.py og bruker to rensefunksjoner under kallet klimagass_rens. 
Scriptet run_rensing kjører hele prosessen. 

Dataen blir renset i følgende steg:
- Renser kolonnenavn, da alle navn og verdier i CSV hadde "" rundt seg
- Gjerner eventuelle duplikatverdier
- Automatisk lagring i data/klimagassutslipp_renset.csv

Disse dataene oppdateres sjeldent, da to ganger i året, og hentes ikke opp gjennom API. Derfor er rensekallet satt opp i en if-setning, ettersom at rensingen er i samme script som rensingen av temperatur som skjer ofte. If-setningen er satt opp slik at om det allerede eksisterer en renset versjon, vil den ikke gjennomføre rensingen på nytt.