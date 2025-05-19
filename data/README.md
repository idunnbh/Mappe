
# Data -- Beskrivelse av filer i 'data/'
Denne mappen inneholder originale datasett, rensede versjoner og testfiler med feil.

## Klimagassutslipp.csv
Dette er en original CSV-fil eksportert manuelt fra SSB. Den inneholder informasjon om klimagassutslippet i Norge fra 1990 til 2023. Den oppdateres to ganger i året og vil oppdateres manuelt. 

Det er denne filen som brukes som input for rensingsscript.

## Klimagassutslipp_norge_renset.csv
Dette er den rensede versjonen av klimagassutslipp.csv. Den genereres automatisk via script i run_rensing.py. Den lagres alltid som klimagassutslipp_renset.csv og lages kun om det ikke finnes en i data/ fra tidligere.

## Klimagassutslipp_verden.csv
Dette er en original CSV-fil henter fra OWID, Our World In Data. Datasettet inneholder kolonner for land, kode, år og det totale årlige klimagassutslipper i CO2-ekvivalenter.

## Klimagassutslipp_verden_renset.csv
Dette er den rensede versjonen av klimagassutslipp_verden.csv. Den er strippet ned og har kun to kolonner: år og det totale årlige klimagassutslipper i CO2-ekvivalenter.

## Historisk_luftkvalitet.csv
Dette er en original CSV-fil hentet fra NILU, Norsk institutt for luftforskning. Målingene er gjort på Elgeseter og har verdier for NO2-, PM10-, og PM2.5-nivå. Det er registrert en gang i timen i 2024.

## Luftkvalitet.json
Inneholder data hentet fra API fra Meterologisk institutt, som blir lagret i en JSON-fil.


## temp_gloshaugen_historisk.csv: 
- Original temperaturdata fra Frost API for 2024 (Gløshaugen)
- Inkluderte fil i Git 

## Ekskludert filer fra Git ( ligger i .gitignore):
Disse filene vil ikke legges til i versjonskontroll. Detter er fordi de enten genereres automatisk, er midlertidige eller brukes til testing. 
- *_renset.csv: Rensede versjoner som genereres i run_rensing.py
- temp_gloshaugen_sanntid_*.csv: Sanntidsdata generert via API-kall
- *inneholder_feil*.csv: Testfiler hvor vi har lagt inn ulike feil for å sjekke rensing

Vi har laget filer med feil for å teste hvordan rensefunksjonene håndterer disse. Testfilene er ignorert med .gitignore.
