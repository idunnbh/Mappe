# Src -- Beskrivelse av filer i 'src/'
Denne mappen inneholder forklaringer og beskrivelser av hvordan vi har hentet inn og bearbeidet dataen.

## Hente og lagre temperaturdata fra MET og Frost API
Her samles det inn og lagres temperaturdata fra to ulike kilder:
1) Sanntidsdata fra MET sitt Locationforecast API (48 timer framover)
2) Historiske data fra Frost API (hver time for hele 2024)

**API-tilganger:**
Scriptet bruker miljøvariabler fra api.env for å hente:
- USER_AGENT: kreves av MET API
- FROST_API_KEY: kreves av Frost API

### Hovedfunksjoner:

**hent_sanntidsdata(lat, lon):** Henter værdata (48 timer frem) for gitt lokasjon fra MET.

**hent_temperaturer(data):** Denne funksjonen brukes for å hente ut tidspunkt og temperatur fra sanntidsdata. Den tar inn et JSON-objekt og returnerer en liste med (tidspunkt, temperatur)-par.

Funksjonens hovedtrekk: 
- Går gjennom alle tidspunktene i værdataene
- For hvert tidspunkt henter det tidspunktet(tid) og temperaturen i lufta (air_temperature)
- Lagrer disse som tupler i en liste

**hent_historiske_temperaturer():** Denne funksjonen henter temperaturdata fra Gløshaugen for hele 2024.

Funksjonens hovedtrekk: 
- Sjekker at API-nøkkel finnes
- Henter data måned for måned for å unngå feil: 
    - Vi prøvde først å hente ut alle tempraturdata for hele 2024 uten en for-løkke, men fikk feil (statuskode 400). Dette er fordi Frost API har en begrensning på hvor mye data som kan returneres per spørring. Derfor laget vi en for-løkke som henter data måned for måned. 
- Henter ut tidspunkt og temperatur fra JSON-responsen
- Filtrering, slik at en måling per time:
    - Da vi først hentet ut tempraturene for 2024, fikk vi nesten 50 000 datapunkter. Dette er fordi noen stasjoner rapporterer oftere enn en gang i timen. For å få et ryddigere og mer oversiktlig datasett, har vi brukt pandas til å filtrere målingene. Nå beholder en måling per time. Dette gjør vi ved å gruppere målingene etter time (resample('1H')) og hente den første verdien for hver time.
    - Returnerer en liste med (tidspunkt, temperatur)-par.

**lagre_til_csv(data, filnavn):** Lagrer listene med (tid, temperatur) til en .csv-fil i data/-mappen.

## Klimagassutslipp
Datasettet som brukes er hentet fra Statistisk sentralbyrå og inneholder data om klimagassutslipp i Norge fra 1990 til 2023. Rådataen ble hentet ut i CSV-fil og hadde små utfordringer knyttet til struktur og format. Filen inneholdt både metadata, kolonnenavn og data i samme fil.

For å arbeide med dataen har vi brukt Pandas til å lese inn og bearbeide CSV-filen. Ved hjelp av os, base_path og filepath finner koden filen relativt i arbeidet, uavhengig hvor den kjøres fra. Deretter filterer vi datatsettet til å kun vise aktivitet "0 Alle kilder" og komponent "Klimagasser i alt", slik at vi får et mer oversiktig datasett å jobbe med videre.

Vi filtrerer så datasettet til å kun vise "0 Alle kilder" og "Klimagasser i alt", slik at vi får et mer oversiktlig datasett å jobbe videre med. Deretter konverterer vi tallverdier fra CSV-filen fra en streng til interger, slik at de vil bli forstått riktig av pandas og matplotlib i framtidig analyse. Om verdiere ikke lar deg konvertere vil de bli satt til NaN (Not a number).

For å bekrefte at koden fungerer har vi brukt print(df.head()) for å printe ut de 5 første linjene. Det fungerte slik vi ønsker. Resultatet ble slik:

----- 

  kilde (aktivitet)          komponent    år  Utslipp til luft (1 000 tonn CO2-ekvivalenter, AR5)
0     0 Alle kilder  Klimagasser i alt  1990                                              51348  
1     0 Alle kilder  Klimagasser i alt  1991                                              48987  
2     0 Alle kilder  Klimagasser i alt  1992                                              47450  
3     0 Alle kilder  Klimagasser i alt  1993                                              49379  
4     0 Alle kilder  Klimagasser i alt  1994                                              51331


------ 

## Luftkvalitet
For å hente inn, rense og kombinere luftkvalitetsdata, er det brukt både API (Meterologisk institutt) og et historisk datasett (CSV-fil fra Norsk institutt for luftforskning, NILU). Dataen fra API-et er sanntidsdata 48 timer fram i tid, og det historiske datasettet er registrerte målinger hver time i 2024. Dette fordi vi tok en vurdering på at vi burde ha mer data å jobbe med.Hovedstrukturen i koden er:
- Hente data fra API-et ved å bruke miljøvariabler for konfigurasjon.
- Lagre rådata som JSON for senere bruk eller feilsøking.
- Normalisere JSON-strukturen til en Pandas DataFrame for videre analyse.
- Hente et historisk datasett (CSV) med luftkvalitetsmålinger og filtrere ut mangelfulle rader.

### Kodeforklaring
- get_air_quality_data(url, params, headers):
    Sender en GET-forespørsel til API-et med de spesifiserte parametrene. Får vi statuskode 200, returneres JSON-svaret. Ellers kastes en exception.

- save_json_data(data, filename):
    Skriver JSON-data til en fil.

- process_air_quality_data(data):
    pd.json_normalize flater ut den nestede JSON-strukturen (under "data" → "time") til en Pandas DataFrame.

- Lese historisk CSV-data:
    Leser et lokalt CSV-datasett (eksportert fra Excel) med semikolon som delimiter, hopper over de 3 første radene som bare var tekst. Deretter lagres en kopi av DataFrame-en i data/historisk_luftkvalitet.csv.

- Filtrere ut rader med 100% dekning:
    Datasettet er mangelfullt, så beholder kun de radene der alle kolonner for dekning er 100.0 for å kun jobbe med rader der alle målingene er fullstendige. .copy() brukes for å unngå SettingWithCopyWarning.

- Konvertere strenger til flyt:
    I Excel-eksporten brukes komma som desimalskille. Vi erstatter komma med punktum og konverterer til float, for at Pandas skal kunne behandle dataene numerisk.

- Sette negative verdier til 0:
    Negative verdier er satt til null, siden vi anser det som sensorstøy eller ugyldig data.



### rensing.py - Rensing av data
Vi har laget en modul med funksjoner for å rense både temperaturdata, klimagassdata og luftkvalitetdate. Rensefunksjonene er delt inn i gjenbrukbare komponenter:


## rensing.py - Rensing av data
Vi har laget en modul med funksjoner for å rense både temperaturdata og klimagassdata. Rensefunksjonene er delt inn i gjenbrukbare komponenter:

**Generelle funksjoner:**
- last_in_csv(filsti): Leser inn en CSV-fil som pandas DataFrame.
- fjern_duplikater(df): Fjerner duplikate rader og gir beskjed om hvor mange som ble fjernet.

**Temperaturspesifikke funksjoner:**
- håndter_manglende_verdier(df, kolonne='temperatur')`: Fyller inn manglende temperaturer med gjennomsnitt.
- fjern_outliers(df, kolonne='temperatur'):Fjerner urealistiske temperaturer (under -50°C eller over 50°C).

**Klimagassspesifikke funksjoner:**
- rense_kolonnenavn(df): Fjerner hermetegn og ekstra mellomrom fra kolonnenavn.

**Kombinerte funksjoner (pipelines):**
- temperatur_rens(df): Brukes for temperaturdata. Den fjerner duplikater, outliers og manglende verdier.
- klimagass_rens(df): Brukes for klimagassdata. Rydder kolonnenavn, fjerner duplikater og sjekker at de nødvendige kolonnene ('kilde (aktivitet)', 'komponent' og 'år') finnes.

## run_rensing.py – Kjøring for rensing av 
I scriptet blir data renset ved at de ulike rensefunksjonene kjøres og den rensete dataen blir lagret som nye CSV-filer.

### Temperaturdata:
I rens_og_lagre_temperaturdata() blir sanntidstemperatur og historiske tempraturer håndtert på ulike måter. 

**For sanntidsdata:**
- data fra data/temp_gloshaugen_sanntid_{dato}.csv blir lest inn 
- temperatur_rens() kjøres for å rense data 
- renset data lagres som data/temp_gloshaugen_sanntid_{dato}_renset.csv

Dette skjer hver gang scriptet kjøres, slik at vi alltid har renset fersk sanntidsdata

**For historisk temperatur:**
- leser inn data fra data/temp_gloshaugen_historisk.csv
- renset versjon lagres som data/temp_gloshaugen_historisk_renset.csv
Rensing skjer kun en gang: Hvis renset fil allerede finnes, hoppes det over

### Klimagassdata:
I rens_og_lagre_klimagassdata() blir den originale CSV-filen data/klimagassutslipp.csv lest inn med sep=";" og skiprows=2 for å hoppe over metadata og hente riktige kolonnenavn.
- Filen rensen med klimagass_rens() 
- Hermetegn rundt navn og duplikater fjernes
- Nødvendige kolonner blir sjekket
- Den rensede dataen lagres som data/klimagassutslipp_renset.csv

Siden klimagassdataen kun oppdateres et par ganger i året, og ikke hentes fra et API, er det lagt inn en if-sjekk i scriptet. Dersom den rensede filen allerede eksisterer, blir rensingen ikke kjørt på nytt. Dette sparer tid, og forhindrer unødvendig behandling hver gang scriptet kjøres.

## generer_feil_i_data.py - lager feil i datasett
For sjekke og vise at funksjonene våre for rensing av data fungerer, har vi laget en versjon av den historiske temperaturdataene som inneholder feil. Vi tok utgangspunkt i data/temp_gloshaugen_historisk.csv og lagde en ny fil som heter data/temp_gloshaugen_historisk_inneholder_feil.csv

**Feilene ble lagt inn med kode på denne måten:**
- Satt 10 tilfeldige temperaturverdier til null, for å få manglende verdier. 
- Erstattet 5 tilfeldige verdier med urealistiske temperaturer. 
- Kopierte og la inn 5 rader som allerede fantes i datasettet.

Funksjonen for rensing av tempratur data, temperatur_rens(), ble deretter kjørt på denne. Den rensede versjon blir lagret som data/temp_gloshaugen_historisk_inneholder_feil_renset.csv.

## Eksempel på output ved kjøring:
Fjernet 0 duplikater.
Fjernet 0 outliers.
Sanntidstemperaturer renset og lagret i: data/temp_gloshaugen_sanntid_2025-03-28_renset.csv      
Fjernet 0 duplikater.
Fjernet 0 outliers.
Historisk temperaturdata renset og lagret i:data/temp_gloshaugen_historisk_renset.csv
Manglende verdier=10.Disser er nå fylt med gjennomsnittet.
Fjernet 5 duplikater.
Fjernet 5 outliers.
Historisk temperaturdata(med feil) renset lagret i:data/temp_gloshaugen_historisk_inneholder_feil_renset.csv
Klimagassdata er allerede renset.

------

Her vises det at funksjonene oppdager og behandler:
10 manglende verdier, 5 duplikater og 5 outliers

Altså fungerer rensingen som forventet!! YEY

------------------------------------------------------------------------ 

# Kilder
Temperaturdata:
1) Meteorologisk institutt. Locationforecast API v2. Hentet fra: https://api.met.no/weatherapi/locationforecast/2.0/documentation
2) Meteorologisk institutt. Frost API. Hentet fra: https://frost.met.no/
Klimagassutslipp:
3) Statistisk sentralbyrå (SSB). Utslipp av klimagasser etter kilde og type. Tabell 13931. Hentet fra: https://www.ssb.no/statbank/table/13931

## Miljøvariabler og API-nøkler:
API-nøkler lastes inn via dotenv fra en lokal .env-fil.
**Brukte variabler:** USER_AGENT og FROST_API_KEY.
