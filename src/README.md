
### Hente og lagre temperaturdata fra MET og Frost API
Her samles det inn og lagres temperaturdata fra to ulike kilder:
1) Sanntidsdata fra MET sitt Locationforecast API (48 timer framover)
2) Historiske data fra Frost API (hver time for hele 2024)

API-tilganger
Scriptet bruker miljøvariabler fra api.env for å hente:
USER_AGENT: kreves av MET API
FROST_API_KEY: kreves av Frost API

Hovedfunksjoner:

hent_sanntidsdata(lat, lon): 
    Henter værdata (48 timer frem) for gitt lokasjon fra MET.

hent_temperaturer(data): 
    Denne funksjonen brukes for å hente ut tidspunkt og temperatur fra sanntidsdata. Den tar inn et JSON-objekt og returnerer en liste med (tidspunkt, temperatur)-par.
    Funksjonens hovedtrekk: 
    -Går gjennom alle tidspunktene i værdataene
    -For hvert tidspunkt henter det tidspunktet(tid) og temperaturen i lufta (air_temperature)
    -Lagrer disse som tupler i en liste

hent_historiske_temperaturer(): 
    Denne funksjonen henter temperaturdata fra Gløshaugen for hele 2024.
    Funksjonens hovedtrekk: 
    - Sjekker at API-nøkkel finnes
    - Henter data måned for måned for å unngå feil: 
        Vi prøvde først å hente ut alle tempraturdata for hele 2024 uten en for-løkke, men fikk feil (statuskode 400). Dette er fordi Frost API har en begrensning på hvor mye data som kan returneres per spørring. Derfor laget vi en for-løkke som henter data måned for måned. 
    - Henter ut tidspunkt og temperatur fra JSON-responsen
    - Filtrering, slik at en måling per time:
        Da vi først hentet ut tempraturene for 2024, fikk vi nesten 50 000 datapunkter. Dette er fordi noen stasjoner rapporterer oftere enn en gang i timen. For å få et ryddigere og mer oversiktlig datasett, har vi brukt pandas til å filtrere målingene. Nå beholder en måling per time. Dette gjør vi ved å gruppere målingene etter time (resample('1H')) og hente den første verdien for hver time.
    - Returnerer en liste med (tidspunkt, temperatur)-par

lagre_til_csv(data, filnavn): 
    Lagrer listene med (tid, temperatur) til en .csv-fil i data/-mappen.


### Klimagassutslipp
Datasettet som brukes er hentet fra Statistisk sentralbyrå (https://www.ssb.no/statbank/table/13931) og inneholder data om klimagassutslipp i Norge fra 1990 til 2023. Rådataen ble hentet ut i CSV-fil og hadde små utfordringer knyttet til struktur og format. Filen inneholdt både metadata, kolonnenavn og data i samme fil.


### rensing.py - Rensing av data
Vi har laget en modul med funksjoner for å rense både temperaturdata, klimagassdata og luftkvalitetdate. Rensefunksjonene er delt inn i gjenbrukbare komponenter:

Generelle funksjoner
    - last_in_csv(filsti): Leser inn en CSV-fil som pandas DataFrame.
    - fjern_duplikater(df): Fjerner duplikate rader og gir beskjed om hvor mange som ble fjernet.

Temperaturspesifikke funksjoner
    - håndter_manglende_verdier(df, kolonne='temperatur')`: Fyller inn manglende temperaturer med gjennomsnitt.
    - fjern_outliers(df, kolonne='temperatur'):Fjerner urealistiske temperaturer (under -50°C eller over 50°C).

Klimagassspesifikke funksjoner
- rense_kolonnenavn(df): Fjerner hermetegn og ekstra mellomrom fra kolonnenavn.

Kombinerte funksjoner (pipelines)
- temperatur_rens(df): Brukes for temperaturdata. Den fjerner duplikater, outliers og manglende verdier.
- klimagass_rens(df): Brukes for klimagassdata. Rydder kolonnenavn og fjerner duplikater.


### run_rensing.py – Kjøring for rensing av 
I scriptet blir data renset ved at de ulike rensefunksjonene kjøres og den rensete dataen blir lagret som nye CSV-filer.

Temperaturdata:
I rens_og_lagre_temperaturdata() blir sanntidstemperatur og historiske tempraturer håndtert på ulike måter. 
For sanntidsdata:
- data fra data/temp_gloshaugen_sanntid_{dato}.csv blir lest inn 
- temperatur_rens() kjøres for å rense data 
- renset data lagres som data/temp_gloshaugen_sanntid_{dato}_renset.csv
Dette skjer hver gang scriptet kjøres, slik at vi alltid har renset fersk sanntidsdata
For historisk temperatur:
- leser inn data fra data/temp_gloshaugen_historisk.csv
- renset versjon lagres som data/temp_gloshaugen_historisk_renset.csv
Rensing skjer kun en gang: Hvis renset fil allerede finnes, hoppes det over

Klimagassdata:
I rens_og_lagre_klimagassdata():
- Automatisk lagring i data/klimagassutslipp_renset.csv
Disse dataene oppdateres sjeldent, da to ganger i året, og hentes ikke opp gjennom API. Derfor er rensekallet satt opp i en if-setning, ettersom at rensingen er i samme script som rensingen av temperatur som skjer ofte. If-setningen er satt opp slik at om det allerede eksisterer en renset versjon, vil den ikke gjennomføre rensingen på nytt.


---

### Kilder
Temperaturdata:
1) Meteorologisk institutt. Locationforecast API v2. Hentet fra: https://api.met.no/weatherapi/locationforecast/2.0/documentation
2) Meteorologisk institutt. Frost API. Hentet fra: https://frost.met.no/
Klimagassutslipp:
3) Statistisk sentralbyrå (SSB). Utslipp av klimagasser etter kilde og type. Tabell 13931. Hentet fra: https://www.ssb.no/statbank/table/13931

**Miljøvariabler og API-nøkler:**
API-nøkler lastes inn via dotenv fra en lokal .env-fil.
Brukte variabler: USER_AGENT og FROST_API_KEY.