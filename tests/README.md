## Tester av datarensing

Har laget enhetstester for funksjonene som renser temperaturdata, for å sikre at de fungerer som forventet.
Testene sjekker følgene ting: 
-fjern_outliers: Sikrer at ekstreme temperaturer fjernes korrekt
-fjern_duplikater: Fjerner duplikate rader basert på tidspunkt
-håndter_manglende_verdier: Erstatter manglende temperaturer med gjennomsnitt
-rens_data: Kjøring av hele renseprosessen samlet

For at testfilene skal finne funksjonene i src/databehandling, legges src-mappa til i Pythons søkesti (sys.path). Dette gjøres slik i starten av test_rensing.py:

```bash
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
```

Positive og negative tester:
Koden bruker både posetive og negative tester. 
-Positive tester sjekker at funksjonene fungerer som forventet når dataene er gyldige.
-Negative tester sjekker hvordan funksjonene håndterer uvanlige eller ekstreme tilfeller, som for eksempel når alle verdier er ugyldige (outliers) og skal fjernes.


Hvordan kjøre testene:
Kjør følgende kommando fra prosjektmappa:
```bash
python -m unittest tests/test_rensing.py

```
Eksempel på output når testene kjøres:

Fjernet 1 duplikater.
Fjernet 1 outliers.
Manglende verdier funnet->fyller med gjennomsnitt.
...
----------------------------------------------------------------------
Ran 5 tests in 0.014s

OK

#Dette viser at alle testene kjørte som forventet og at funksjonene for datarensing fungerer som den skal. 


