# Src -- Beskrivelse av filer i 'src/'
Denne mappen inneholder forklaringer og beskrivelser av hvordan vi har hentet inn, bearbeidet, analysert og visualisert data.

## Innholdsfortegnelse
- [datainnsamling_tempratur.py](#datainnsamling_tempraturpy)
- [datainnsamling_klimagassutslipp.py og datainnsamling_klimagassutslipp_verden.py](#datainnsamling_klimagassutslipppy-og-datainnsamling_klimagassutslipp_verdenpy)
- [datainnsamling_luftkvalitet.py](#datainnsamling_luftkvalitetpy)
- [rensing.py](#rensingpy)
- [run_rensing.py](#run_rensingpy)
- [generer_feil_i_data.py](#generer_feil_i_datapy)
- [statistikk.py](#statistikkpy)
- [kilmagass_visualisering.py](#kilmagass_visualiseringpy)
- [temp_visualisering.py](#temp_visualiseringpy)
- [Kilder](#kilder)
- [Miljøvariabler og API-nøkler](#miljøvariabler-og-api-nøkler)


------------------------------------------------------------------------ 

## datainnsamling_tempratur.py
[Åpne fil->](datainnsamling_tempratur.py)

I datainnsamling_tempratur.py blir det hentet og lagrer temperaturdata fra MET og Frost API
Her samles det inn og lagres temperaturdata fra to ulike kilder:
1) Sanntidsdata fra MET sitt Locationforecast API (48 timer framover)
2) Historiske data fra Frost API (hver time for x antall år, her 50år)

**API-tilganger:**
Scriptet bruker miljøvariabler fra api.env for å hente:
- USER_AGENT: kreves av MET API
- FROST_API_KEY: kreves av Frost API

### Funksjoner i datainnsamling_tempratur.py:

**hent_sanntidsdata(lat, lon):** 
- Henter værdata (48 timer frem) for en gitt lokasjon fra MET.

**hent_temperaturer(data):** 
- Denne funksjonen brukes for å hente ut tidspunkt og temperatur fra sanntidsdata. Den tar inn et JSON-objekt og returnerer en liste med (tidspunkt, temperatur)-par.

**hent_historiske_temperaturer(antall_år=50):**
- Denne funksjonen henter historiske temperaturdata fra Frost API for de siste antall_år (standard: 50 år tilbake). 
- Funksjonen: 
    - Sjekker at API-nøkkel finnes
    - Tidsintervall blir tilpasset ved at startår regnes ut basert på dagens år og valgt antall år tilbake.
    - Henter data måned for måned for å unngå feil: 
        Vi prøvde først å hente ut alle tempraturdata for hele 2024 uten en for-løkke, men fikk feil (statuskode 400). Dette er fordi Frost API har en begrensning på hvor mye data som kan returneres per spørring. Derfor laget vi en for-løkke som henter data måned for måned. 
    - Henter ut tidspunkt og temperatur fra JSON-responsen
    - Filtrering, slik at en måling per time:
        Da vi først hentet ut tempraturene for 2024, fikk vi nesten 50 000 datapunkter. Dette er fordi noen stasjoner rapporterer oftere enn en gang i timen. For å få et ryddigere og mer oversiktlig datasett, har vi brukt pandas til å filtrere målingene. Nå beholder en måling per time. Dette gjør vi ved å gruppere målingene etter time (resample('1h')) og hente den første verdien for hver time.
    - Returnerer en liste med (tidspunkt, temperatur)-par


**lagre_til_csv(data, filnavn):** Lagrer listene med (tid, temperatur) til en .csv-fil i data/-mappen.

------------------------------------------------------------------------ 

## datainnsamling_klimagassutslipp.py og datainnsamling_klimagassutslipp_verden.py 

### datainnsamling_klimagassutslipp.py 
[Åpne fil->](datainnsamling_klimagassutslipp.py)
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

### datainnsamling_klimagassutslipp_verden.py 
[Åpne fil->](datainnsamling_klimagassutslipp_verden.py)
Datasettet som brukes her er hentet fra nettstedet Our World in Data (OWID). Dataen inneholder globale klimagassutslipp fra 1973 til 2023, målt i CO2-ekvivalenter, lik som det norske datasettet. Dataen blir hentet ved hjelp av en åpen Data API (CSV-lenke) fra OWID, som gir oss tilgang til oppdaterte datasett direkte, uten behov for API-nøkkel.

Vi bruker pandas.read_csv() med en tilpasset User-Agent for å hente fila direkte fra nettstedet. Slik så de 5 første linjene ut i et originale datasettet:

-----

Entity,Code,Year,Annual greenhouse gas emissions in CO₂ equivalents
World,OWID_WRL,1973,30340880000
World,OWID_WRL,1974,30245190000
World,OWID_WRL,1975,30411125000
World,OWID_WRL,1976,31535469000

-----

Det originale datasettet var ryddig og strukturert, men overskriftene var på engelsk og det var to unødvendige kolonner i forhold til filtreringene gjort før API-en var lastet ned. Under rensingen justerte vi dette med å oversette overskriftene og ta vekk de to første kolonnene. Resultatet etter rensingen så slik ut:

-----

År,Utslipp i CO2 ekvivalenter
1973,30340880000
1974,30245190000
1975,30411125000
1976,31535469000

-----

------------------------------------------------------------------------ 

## datainnsamling_luftkvalitet.py 
[Åpne fil->](datainnsamling_luftkvalitet.py)
For å hente inn, rense og kombinere luftkvalitetsdata, er det brukt både API (Meterologisk institutt) og et historisk datasett (CSV-fil fra Norsk institutt for luftforskning, NILU). Dataen fra API-et er sanntidsdata 48 timer fram i tid, og det historiske datasettet er registrerte målinger hver time i 2024. Dette fordi vi tok en vurdering på at vi burde ha mer data å jobbe med.Hovedstrukturen i koden er:
- Hente data fra API-et ved å bruke miljøvariabler for konfigurasjon.
- Lagre rådata som JSON for senere bruk eller feilsøking.
- Normalisere JSON-strukturen til en Pandas DataFrame for videre analyse.
- Hente et historisk datasett (CSV) med luftkvalitetsmålinger og filtrere ut mangelfulle rader.

### Funksjoner i datainnsamling_luftkvalitet.py 
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

------------------------------------------------------------------------ 

## rensing.py
[Åpne fil->](rensing.py) 
Dette scriptet inneholder funksjoner som skal rense temperatur- og klimagassdata før videre analyse.

**Generelle funksjoner:**
- last_in_csv(filsti): Leser inn en CSV-fil som en pandas DataFrame.
- fjern_duplikater(df): Fjerner duplikate rader og gir beskjed om hvor mange som ble fjernet.

**Temperaturspesifikke funksjoner:**
- finn_gjennomsnittstemperatur(df):  Henter ut gjennomsnittet av kolonnen temperatur ved hjelp av SQL (pandasq)
- håndter_manglende_verdier(df, kolonne='temperatur')`: Fyller inn manglende temperaturer med gjennomsnitt.
- fjern_outliers(df, kolonne='temperatur'):Fjerner urealistiske temperaturer (under -50°C eller over 50°C).

**Klimagassspesifikke funksjoner:**
- rense_kolonnenavn(df): Fjerner hermetegn og ekstra mellomrom fra kolonnenavn i det norske klimagass-settet.

**Kombinerte funksjoner:**
- temperatur_rens(df): Brukes for temperaturdata. Den fjerner duplikater, outliers og manglende verdier.
- klimagass_rens(df): Brukes for klimagassdata. Rydder kolonnenavn, fjerner duplikater og sjekker at de nødvendige kolonnene ('kilde (aktivitet)', 'komponent' og 'år') finnes.

### Hvorfor bruke pandasql?
I finn_gjennomsnittstemperatur(df) brukers pandasql for å kjøre en SQL-spørring direkte på Pandas-dataframes. Dette gjør lesbarheten bedre og det vil være enklere å manipulere data senere. Ved å bruke pandasql her blir det enklere å hente ut gjennomsnittstemperatur på strukturert måte. SQL vil også flere situasjoner være mer oversiktlig enn lange Pandas-kjeder.

------------------------------------------------------------------------ 

## run_rensing.py 
[Åpne fil->](run_rensing.py)
I scriptet blir data renset ved at de ulike rensefunksjonene kjøres og den rensete dataen blir lagret som nye CSV-filer.

**For sanntidsdata:**
- data fra data/temp_gloshaugen_sanntid_{dato}.csv blir lest inn 
- temperatur_rens() kjøres for å rense data 
- renset data lagres som data/temp_gloshaugen_sanntid_{dato}_renset.csv

Dette skjer hver gang scriptet kjøres, slik at vi alltid har renset ny sanntidsdata

**For historisk temperatur:**
- leser inn data fra data/temp_gloshaugen_historisk_{antall_år}år.csv
- renset versjon lagres som data/temp_gloshaugen_historisk_renset_ {antall_år}.csv
Rensing skjer kun en gang: Hvis renset fil allerede finnes, hoppes det over

**For Klimagassdata:**
 den originale CSV-filen data/klimagassutslipp.csv lest inn med sep=";" og skiprows=2 for å hoppe over metadata og hente riktige kolonnenavn.
- Filen rensen med klimagass_rens() 
- Hermetegn rundt navn og duplikater fjernes
- Nødvendige kolonner blir sjekket
- Den rensede dataen lagres som data/klimagassutslipp_renset.csv

Siden klimagassdataen kun oppdateres et par ganger i året, og ikke hentes fra et API, er det lagt inn en if-sjekk i scriptet. Dersom den rensede filen allerede eksisterer, blir rensingen ikke kjørt på nytt. Dette sparer tid, og forhindrer unødvendig behandling hver gang scriptet kjøres.

------------------------------------------------------------------------ 

## generer_feil_i_data.py 
[Åpne fil->](generer_feil_i_data.py)
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

## statistikk.py
[Åpne fil->](statistikk.py)
statistikk.py inneholder funksjoner for å analysere de ulik datasettene.

### Funksjoner i statistikk.py

**Hjelpefunksjoner**

rens_kolonnenavn(df)
-Renser kolonnenavn ved å fjerner mellomrom og spesialtegn og gjør alt til små bokstaver.

legg_til_tid(df, tidkolonne="tid", groupby=None)
- Legger til kolonner for dato, år, måned og time basert på en tid-kolonne.
- Hvis tidkolonnen bare inneholder årstall (heltall), legges kun år til og hvis groupby er lik "år", fjernes måned og time 

finn_kildekolonne(df)
-Finner kolonnen som inneholder ordet "kilde", som brukes til senere.

**Analysefunksjoner**

analyser_fil(filsti, sep=',', datokolonne=None, groupby='måned')
- Leser inn CSV-fil, rydder opp kolonnenavn og grupperer data per år/måned/kilde.
- Gjør enkle statistikke beregninger (gjennomsnitt, median og eventuelt standardavvik) for numeriske variabler. Standardavvik blir bare regnet ut hvis det er mer enn ett datapunkt i hver gruppe.
- Den returnerer 3 ting: 
    - statistikk = Samlede beregninger.(En dictionary, der nøkkelen er kolonnenavnet på den målte variabelen, og verdien er en df med samlet statistikk (gjennomsnitt, median, evt. standardavvik))
    - df_total = Kun totalverdier hvis de finnes, f.eks. "alle kilder" (Returnerer None hvis det ikke finnes).
    - df = hele det ferdig ryddede datasettet (Alle kolonner fra datasettet, rensede kolonnenavn, tid-kolonnen konvertert til datetime-format)

analyser_temperatur(filsti, dataanalysemodul, datokolonne="tidspunkt", groupby="måned")
Bygger vidrer på analyser_fil. Siden temperaturdata inneholder målinger for de første månedene av 2025 vil dette gi misvisende statistikk.
For tempraturdata må det derfor gjøres en ekstra kontroll slik at kun år med fullstendig data (alle 12 måneder) tas med i beregningene.
- Bygger videre på analyser_fil.
- Brukes for temperaturdata, hvor man må filtrere ut år som ikke har data for alle 12 måneder.
- Returnerer samlet statistikk (gjennomsnitt, median, standaravik) og årlige gjennomsnitt for hele år.

beregn_endring_totalt(df, årskolonne='år', verdikolonne='årsgjennomsnitt')
- Beregner total endring fra første til siste år, både som absolutt endring og prosentvis endring. Denne brukes for å se utvikling over tid.

beregn_endring_årlig(df, årskolonne='år', verdikolonne='årsgjennomsnitt')
- Beregner endringen fra ett år til neste, både i absolutte tall og prosentvis. Dette gir mer detaljert oversikt over utviklingen over tid. 

ekstremverdier(df, årskolonne='år', verdikolonne='gjennomsnitt')
- Finner året med høyest og året med lavest verdi.

tiår_snitt(df, årskolonne='år', verdikolonne='gjennomsnitt')
-Grupperer dataen i tiårsperioder og regner ut gjennomsnitt av disse perioden.

beregn_avvik(df, årskolonne='år', verdikolonne='årsgjennomsnitt')
- Legger til en ny kolonne som viser avviket fra totalgjennomsnittet for hver rad i datasettet. Dette er nyttig for å finne unormale år.

analyser_utslipp_norge(df, årskolonne='år', kildekolonne='kilde_(aktivitet)')
- Brukes for å analysere utslipp i Norge. Beregner gjennomsnitt og median per kilde per år og fjerner "alle kilder".

gjennomsnitt_per_kilde(df, kildekolonne='kilde_(aktivitet)', årskolonne='år')
- Finner gjennomsnitt og median for hver kilde over alle år. Brukes for å rangere hvilken kilde som slipper ut mest.

lag_totaldata(df_total, årskolonne='år')
- Finner år og totalutslipp fra en datastruktur og renser kolonnenavn for at dataen kan brukes videre.

beregn_endring_per_kilde(df, aktivitetskolonne='kilde_(aktivitet)', årskolonne='år', verdikolonne='mean')
- Beregner årlig endring for hver enkelt kilde.

analyser_luftkvalitet(df_luft, målinger)
- Regner ut daglig, månedlig og årlig snitt for hvert stoff. Bruker også ekstremverdier() for å finne høyeste og laveste måling for hver kilde.

------------------------------------------------------------------------ 

## kilmagass_visualisering.py
[Åpne fil->](klimagass_visualisering.py)
Denne filen inneholder funksjoner for å visualisere klimagassutslipp. 

### Funksjoner i  kilmagass_visualisering.py:

def plot_utslipp(df, datokolonne, verdi_kolonne, tittel, ax, fig, farge): 
- Lager et linjediagram som viser utviklingen i utslipp per år.

def plot_utslipp_per_tiar(df, tittel):
- Lager et stolpediagram som viser gjennomsnitt per tiår.

def plot_norge_og_verden_sammen(df_norge, df_verden, verdi_kolonne_norge, verdi_kolonne_verden):
- Plotter utslipp i Norge og verden i samme graf med to y-akser.

def plot_norge_og_verden_separat(df_norge, df_verden):
- Plotter utslipp i Norge og verden i to separate grafer ved siden av hverandre.

def plot_utslipp_per_kilde(df, datokolonne, gruppering, verdi_kolonne):
- Lager et linjediagram som viser utviklingen i utslipp for hver enkelt kilde over tid.

def plot_andel_per_kilde(df, år, årskolonne, kildekolonne, utslippkolonne):
- Lager et kakediagram som viser andelen av totale utslipp per kilde for ett valgt år.

def plot_heatmap_per_kilde(df):
- Lager et heatmap som viser utslipp per kilde og år, hvor fargen sier nooe om hvor mye utslipp hver sektor har.

-----------------------------------------------------------------------

## temp_visualisering.py
[Åpne fil->](temp_visualisering.py)
Denne filen inneholder funksjoner for å visualisere tempraturdata. 

### Funksjoner i  temp_visualisering.py:

- plot_interactive_bokeh(df):  
    Interaktivt linjeplot av årlig gjennomsnittstemperatur med hover-effekt og markering av varmeste og kaldeste år (Bruker Bokeh).

- plot_by_decade(df):  
    Søylediagram som viser gjennomsnittlig temperatur per tiår.

- plot_temperatur_år(df):  
    Enkelt linjeplot for temperaturutvikling år for år (Matplotlib).

- plot_avvik(df):  
    Visualiserer avvik fra totalgjennomsnitt som farget barplot (blå for kaldere, rød for varmere).

- tegn_endring_sol(filsti):  
    En sol med stråler og tekst som viser hvor mye temperaturen har økt i datasettet.

- plot_sanntids_temperatur
    Viser temperatur for kommende dager basert på sanntidsdata fra MET.
    Funksjonen varsler også dersom det er meldt veldig varmt (over 25°C) eller veldig kaldt (under 0°C).

------------------------------------------------------------------------ 

# Kilder
Temperaturdata:
1) Meteorologisk institutt. Locationforecast API v2. Hentet fra: https://api.met.no/weatherapi/locationforecast/2.0/documentation
2) Meteorologisk institutt. Frost API. Hentet fra: https://frost.met.no/
Klimagassutslipp:
3) Statistisk sentralbyrå (SSB). Utslipp av klimagasser etter kilde og type. Tabell 13931. Hentet fra: https://www.ssb.no/statbank/table/13931
4) https://ourworldindata.org/co2-and-greenhouse-gas-emissions#all-charts


## Miljøvariabler og API-nøkler:
API-nøkler lastes inn via dotenv fra en lokal .env-fil.
**Brukte variabler:** USER_AGENT og FROST_API_KEY.
