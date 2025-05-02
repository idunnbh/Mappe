# notebooks -- Beskrivelse av filer i 'notebooks/'
Denne mappen inneholder notebooks som brukes til analyse, prediktiv modellering og visualisering av temperatur-, klimagass- og luftkvalitetsdata.


## dataanalyse.ipynb
I notebooken vises det hvordan funksjonene fra statistikk.py brukes til å analysere og strukturere de ulike datasettene:

- Temperaturdata (`temp_gloshaugen_historisk_renset_ 50.csv`)
- Klimagassutslipp (`klimagassutslipp_norge_renset.csv`) og (`klimagassutslipp_verden_renset.csv`)
- Luftkvalitet (`gyldig_historisk_luftkvalitet.csv`)

Først analyseres temperaturdata for å undersøke utviklingen over tid, både årlig og per tiår.
Deretter analyseres globale utslipp for å få oversikt over utviklingen i verden.
Videre undersøkes utslipp i Norge, fordelt på ulike kilder.
Til slutt analyseres luftkvalitetsmålinger for å finne utviklingen av stoffene over tid.


## prediktiv_analyse.ipynb
Denne notebooken tar for seg en predektiv analyse med lineær regresjon.

### Datagrunnlag
- **Temperaturdata:** Data er hentet fra data/temp_gloshaugen_historisk_renset_ 50.csv
- **Klimagassdata:** Data er hentet fra data/klimagassutslipp_verden_renset.csv

### Innhold - Hva gjør notebooken?
- Leser inn og slår sammen temperaturdata og klimagassutslippdata
- Lager scatterplots for visuell vurdering
- Lager regresjonsmodell i scatterplott for visuell vurdering
- Lager og trener en lineær regresjonsmodell
- Predikerer fremtidige temperaturer
- Analyse om vi kan nå parisavtalens mål

### Resultater
- R2-verdi: 0.26619619639020997
- MSE-verdi: 0.710210242216765

### Konklusjon


### Forklaringer av funksjoner
- sns.regplot() beregner automatisk en regresjonslinje basert på informasjonen den er gitt, ved hjelp av lineær regresjon

### Om R2 og MSE

- **R^2 (R2):** Hvor godt dataene passer sammen kan tallfestes med R^2. Verdien går fra 0 til 1 (eller 0% til 100%), og destro høyere det er, jo bedre.
- **MSE (Mean Squared Error):** Oversatt som midlere kvadratisk feil. Det er en modell som måler hvor store feil en regresjonsmodell kan gjøre. Desto lavere tallet er, desto mer presis er modellen. Det er gjennomsnittet av kvadrerte avvik mellom faktiske og predikerte verdier.


## visualisering.ipynb
Her visualiseres den analyserte dataen, ved hjelp av Matplotlib, Seaborn, Widgets og Bokeh. Notebooken inneholder ulike typer diagrammer for temperatur, klimagassutslipp og luftkvalitet. 

### Temperatur
For tempraturdata visualiseres utviklingen de siste 50 årene fra Gløshaugen.
Grafene er laget med funksjoner fra temp_visualisering.py, og dataene hentes fra filen temp_gloshaugen_historisk_renset_ 50.csv.
I notatboken er det skrevet refleksjoner og tolkninger i markdown. Det brukes flere ulike graf-typer:
**Interaktivt linjediagram med Bokeh:**
Viser årlig gjennomsnittstemperatur. Brukeren kan zoome og navigere i grafen, og verdier vises med hover. Varmeste og kaldeste år er også markert.
**Søylediagram per tiår:**
Viser gjennomsnittstemperatur for hvert tiår og gjør den langsiktige utviklingen tydeligere. Her brukes Matplotlib og Seaborn.
**Sol-graf:**
En figur som viser total temperaturøkning som en sol. Tallet i midten viser endringen i grader. 

### Klimagassutslipp
For klimagassutslipp visualiseres og analyseres utviklingen i Norge og globalt. Gjennom ulike visualiseringer analyseres endringer over tid og forskjeller mellom sektorer.
Visualiseringene er laget ved hjelp av funksjoner definert i klimagass_visualisering.py, som blir importert via analyser_fil i statistikk.py.
Funksjonene brukes til å generere grafene som presenteres i denne delen av notebooken.

**Konklusjon**
Analysen viser blant annet at Norges klimagassutslipp har gått ned de siste årene, spesielt etter 2020, mens globale utslipp fortsatt å øke. Flere sektorer i Norge, som industri, olje- og gassutvinning og veitrafikk, har redusert sine utslipp over tid.


### Luftkvalitet
#### Linjediagram
Dette skal utbedres
