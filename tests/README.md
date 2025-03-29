# Enhetstester for datarensing

**Positive og negative tester:**
Koden bruker både posetive og negative tester. 
- Positive tester sjekker at funksjonene fungerer som forventet når dataene er gyldige.
- Negative tester sjekker hvordan funksjonene håndterer uvanlige eller ekstreme tilfeller, som for eksempel når alle verdier er ugyldige (outliers) og skal fjernes.

## Temperaturdata
Vi har laget enhetstester for funksjonene som renser temperaturdata, for å sikre at de fungerer som forventet.

Testene sjekker følgene ting: 
- fjern_outliers: Sikrer at ekstreme temperaturer fjernes korrekt
- fjern_duplikater: Fjerner duplikate rader basert på tidspunkt
- håndter_manglende_verdier: Erstatter manglende temperaturer med gjennomsnitt
- rens_data: Kjøring av hele renseprosessen samlet

For at testfilene skal finne funksjonene i src/databehandling, legges src-mappa til i Pythons søkesti (sys.path). Dette gjøres slik i starten av test_rensing.py:

```bash
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
```

### Hvordan kjøre testene:
Kjør følgende kommando fra prosjektmappa:

```bash
python -m unittest tests/test_rensing.py

```

**Eksempel på output når testene kjøres:**

Fjernet 1 duplikater.
Fjernet 1 outliers.
Manglende verdier funnet->fyller med gjennomsnitt.
...
----------------------------------------------------------------------
Ran 5 tests in 0.014s

OK

--------------

**Dette viser at alle testene kjørte som forventet og at funksjonene for datarensing fungerer som den skal.**


## Klimagassdata
Vi har laget enhetstester for funksjoner som renser klimagassdataen. Dette er for å sikre at de fungerer. Testene sjekker følgende:
- rense_kolonnenavn: Fjerner hermetegn og mellomrom mellom kolonnenavn
- last_in_csv: Sjekker at CSV-data blir lest opp riktig og i DataFrame form
- klimagass_rens: Stopper med feilmelding om nødvendig kolonne mangler

For at testfilene skal finne funksjonene i src/databehandling, legges src-mappa til i Pythons søkesti (sys.path). Dette gjøres slik i starten av test_klimagass.py:

```bash
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
```

### Hvordan kjøre testene:
Kjør følgende kommando fra testmappa:

```bash
python -m unittest tests/test_klimagass.py
```

**Eksempel på output når koden kjøres:**

...
----------------------------------------------------------------------
Ran 3 tests in 0.015s

OK

**Dette viser at testene kjøres som forventet og at funksjonene fungerer som de skal.**

## Luftkvalitetsdata
Vi har laget enhetstester for funksjonene som renser temperaturdata, for å sikre at de fungerer som forventet. Testene sjekker følgende:
- test_fetch_success: Verifiserer at fetch_air_quality_data returnerer en ordbok (dict) ved et vellykket API-kall.
- test_fetch_failure: Sjekker at funksjonen kaster en Exception dersom en ugyldig URL brukes.

For at testfilen skal finne funksjonen i src/datainnsamling_luftkvalitet, legges src-mappen til i Pythons søkesti (sys.path). Dette gjøres slik i starten av test_datainnsamling_luftkvalitet.py:

```bash
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
```
### Hvordan kjøre testene
Naviger til testmappen og kjør følgende kommando:
```bash
python -m unittest tests/test_datainnsamling_luftkvalitet.py
```

**Eksempel på output når koden kjøres:**

...
----------------------------------------------------------------------
Ran 2 tests in 0.015s

OK

**Dette viser at testene kjøres som forventet og at funksjonene fungerer som de skal.**