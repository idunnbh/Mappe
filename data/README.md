
Denne mappen inneholder originale datasett, rensede versjoner og testfiler med feil.

### Inkluderte filer i Git:
-temp_gloshaugen_historisk.csv: Original temperaturdata fra Frost API for 2024 (Gløshaugen)
-klimagassutslipp.csv: Klimagassdata fra SSB
-historisk_luftkvalitet.csv: Luftkvalitet-data fra Miljødirektoratet
-luftkvalitet.json: Rådata om luftkvalitet i JSON-format (fra API)

### Ekskludert filer fra Git ( ligger i .gitignore):
Disse filene vil ikke legges til i versjonskontroll. Detter er fordi de enten genereres automatisk, er midlertidige eller brukes til testing. 
-*_renset.csv: Rensede versjoner som genereres i run_rensing.py
-temp_gloshaugen_sanntid_*.csv: Sanntidsdata generert via API-kall
- *inneholder_feil*.csv: Testfiler hvor vi har lagt inn ulike feil for å sjekke rensing

Vi har laget filer med feil for å teste hvordan rensefunksjonene håndterer disse. Testfilene er ignorert med .gitignore.