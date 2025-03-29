# Data -- Beskrivelse av filer i 'data/'

## Klimagassutslipp.csv
Dette er en original CSV-fil eksportert manuelt fra SSB. Den inneholder informasjon om klimagassutslippet i Norge fra 1990 til 2023. Den oppdateres to ganger i året og vil oppdateres manuelt. 
Filstruktur:
    - Første linje: Metadata
    - Andre linje: Kolonnenavn
    - Separator: Semikolon (;)
    - Tekstverdier omgitt av doble anførselstegn ("")
Det er denne filen som brukes som input for rensingsscript.

## Klimagassutslipp_renset.csv
Dette er den rensede versjonen av klimagassutslipp.csv. Den genereres automatisk via script i run_rensing.py. Den lagres alltid som klimagassutslipp_renset.csv og lages kun om det ikke finnes en i data/ fra tidligere.
Filstruktur:
    - Første linje: Kolonnenavn
    - Seperator: Komma (,)
    - Har fjernet anførselstegn rundt navn ("")
    - Har fjernet eventuelle duplikater

## Historisk_luftkvalitet.csv


## Luftkvalitet.json


## Temp_gloshaugen_historisk.csv


## Temp_gloshaugen_historisk_renset.csv