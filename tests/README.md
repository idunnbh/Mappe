# Tests -- Beskrivelse av filer i 'tests/'
Denne mappen inneholder enhetstester som verifiserer at funksjonene for datarensing, innhenting og behandling av dataen fungerer. 

## Innholdsfortegnelse
- [Positive og negative tester](#positive-og-negative-tester)
- [test_temperatur.py](#test_temperaturpy)
- [test_klimagassdata.py](#test_klimagassdatapy)
- [test_luftkvalitet.py](#test_luftkvalitetpy)
- [test_rensing.py](#test_rensingpy)


## Positive og negative tester
- Positive tester sjekker at funksjonene fungerer som forventet når dataene er gyldige.
- Negative tester sjekker hvordan funksjonene håndterer uvanlige eller ekstreme tilfeller, som for eksempel når alle verdier er ugyldige (outliers) og skal fjernes.

## test_temperatur.py
[Åpne fil ->](test_temperatur.py)
Denne filen inneholder enhetstester for funksjoner knyttet til henting og rensing ac temperaturdata fra MET og Frost API. Testene er organisert i tre klasser, som fokuserer på ulike deler av temperaturbehandlingen.

TestTemperaturHenting tester funksjoner knyttet til innhenting av sanntids- og historiske temperaturdata. Den sjekker at sanntidsdata returneres i riktig format (en ordbok med nøkkelen properties). Det blir også kontrolert at API-nøkler (USER_AGENT og FROST_API_KEY) finnes i miljøvariabler, og at evt. feil blir håndtert riktig. Det testes også at dataen som hentes faktisk inneholder temperaturmålinger i form av tidspunkt og temperatur.

TestTemperaturParsing tester om funksjonen hent_temperaturer() tolker JSON-strukturen fra MET API. I testen brukes eksempeldata (dummydata) med samme form som værdata fra API-et vanligvis har. Dette gjør at man kan teste funksjonen uten å være koblet til API-et. Testen kontrollerer at hent_temperaturer() klarer å hente ut riktig informasjon, og at resultatet blir en liste der hvert element er et par med tidspunkt og temperatur.

TestTemperaturRensing tester funksjonen temperatur_rens, som fjerner duplikater, outliers og manglende verdier fra et datasett. Det brukes et eksempel på et datasett som inneholder duplikater og manglende verdier for å kontrollere at funksjonen gjør som forventet.

**Eksempel på output når koden kjøres:**

..Sanntidsdata hentet!
.Sanntidsdata hentet!
..Manglende verdier=1. Disser er nå fylt med gjennomsnittet:15.0
Fjernet 1 duplikater.
Fjernet 0 outliers.
.
----------------------------------------------------------------------
Ran 6 tests in 0.193s

**Dette viser at testene kjøres som forventet og at funksjonene fungerer som de skal.**

## test_klimagassdata.py
[Åpne fil ->](test_klimagassdata.py)
Vi har laget enhetstester for funksjoner som renser klimagassdataen. Dette er for å sikre at de fungerer. Testene sjekker følgende:
- Funksjonen test_klimagass_rens_norge() sjekker at datasettet inneholder riktige kolonner, kilde (aktivitet), komponent og år. Eksempeldataet som brukes:
Olje- og gassutvinning, Klimagasser i alt, 1990.
Her testes det at datasettet behandles uten feil, og at radene beholdes.
- Funksjonen test_klimagass_rens_verden() er en integrasjonstest. I testen blir det opprettet en midlertidig csv-fil med eksempeldata og lagrer den lokal i data-mappen. Derreter kaller funksjonen rens_og_lagre_klimagass_verden() og sjekker at den rensede filen blir opprettet, at den kun inneholder de kolonnene som er relevante (År og utslipp i CO2 ekvivalenter) og at verdiene i filen er riktige og i forventet format.
Testen bruker tempfile.TemporaryDirectory() for å opprette en midlertidig mappe.Dette gjør at alle filer som blit opprettes i testen slettes automatisk etterpå. 
- I test_mangler_kolonne(self): Er det et ugyldig datasett som mangler en nødvendige kolonnene. Her skal funksjonen kaste en KeyError.
- last_in_csv: Sjekker at CSV-data blir lest opp riktig og i DataFrame form

For at testfilene skal finne funksjonene i src/databehandling, legges src-mappa til i Pythons søkesti (sys.path). Dette gjøres slik i starten av test_klimagass.py:

```bash
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
```

**Eksempel på output når koden kjøres:**

Fjernet 0 duplikater.
.Renset data lagret i data/klimagassutslipp_verden_renset.csv
...
----------------------------------------------------------------------
Ran 4 tests in 0.054s

**Dette viser at testene kjøres som forventet og at funksjonene fungerer som de skal.**

## test_luftkvalitet
[Åpne fil ->](test_luftkvalitet.py)
Vi har laget enhetstester for funksjonene som renser luftkvalitetdata, for å sikre at de fungerer som forventet. Testene sjekker følgende:
- test_fetch_success: Verifiserer at fetch_air_quality_data returnerer en ordbok (dict) ved et vellykket API-kall.
- test_fetch_failure: Sjekker at funksjonen kaster en Exception dersom en ugyldig URL brukes.


**Eksempel på output når koden kjøres:**

...
----------------------------------------------------------------------
Ran 2 tests in 0.015s

OK

**Dette viser at testene kjøres som forventet og at funksjonene fungerer som de skal.**

## test_rensing.py 
[Åpne fil ->](test_rensing.py)
Denne filen inneholder enhetstester for funksjonene som renser ulike typer data. Disse funksjonen er gennerelle og kan brukes til rensing av ulike type datasett. 

Testene sjekker følgene funksjoner: 
- fjern_outliers: Tester at ekstreme verdier fjernes
- fjern_duplikater: Tester at duplikate rader basert på tidspunkt fjernes
- håndter_manglende_verdier: Tester at manglende verdier erstattes med gjennomsnitt
- rense_kolonnenavn(): Tester at hermetegn og unødvendige mellomrom fjernes fra kolonnenavn

**Eksempel på output når testene kjøres:**

Fjernet 1 duplikater.
.Fjernet 1 outliers.
.Fjernet 1 outliers.
.Manglende verdier=1. Disser er nå fylt med gjennomsnittet:15.0
..
----------------------------------------------------------------------
Ran 5 tests in 0.052s

OK

**Dette viser at alle testene kjørte som forventet og at funksjonene for datarensing fungerer som den skal.**
