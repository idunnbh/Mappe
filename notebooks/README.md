# notebooks -- Beskrivelse av filer i 'notebooks/'
Denne mappen inneholder notebooks som brukes til analyse, prediktiv modellering og visualisering av temperatur-, klimagass- og luftkvalitetsdata.

## Innholdsfortegnelse

- [data-app](#data-app) – 'App' med widgets for utforsking av miljødata
- [dataanalyse.ipynb](#dataanalyseipynb) – Analyse av temperatur, klimagassutslipp og luftkvalitet  
- [prediktiv_analyse.ipynb](#prediktiv_analyseipynb) – Lineær regresjon og fremtidsprediksjoner  
- [visualisering.ipynb](#visualiseringipynb) – Grafisk fremstilling med Matplotlib, Seaborn og Bokeh

## data-app.ipynb
data-app.ipynb er en interaktiv Jupyter-notatbok som lar brukeren velge hvilke visualiseringer som skal vises. Den kombinerer klimagassutslipp, temperaturmålinger fra Gløshaugen og luftkvalitet fra Elgeseter.
Appen gir også mulighet for å vise prediktive analyser som illustrerer mulige sammenhenger mellom temperatur og miljøpåvirkning.

Notatboken bruker funksjoner fra app_funksjoner.py, og og bruker widgets og data som er definert i widgets_app.py

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
Denne notebooken utfører to analyser:
1. En predektiv analyse med lineær regresjon, hvor vi ser på sammenhengen mellom det globale CO2-ekvivalent-utslippet og temperaturer i Norge.
2. En undersøkelse av sammenhengen mellom temperaturer og luftkvalitetsnivåer i Elgeseter, Trondheim.

### Datagrunnlag
- Temperaturdata (`temp_gloshaugen_historisk_renset_ 50.csv`)
- Klimagassutslipp (`klimagassutslipp_verden_renset.csv`)
- Luftkvalitet (`gyldig_historisk_luftkvalitet.csv`)

### Prediktiv analyse med lineær regresjon
**Utførelse:**
- Leser inn og slår sammen temperaturdata og klimagassutslippdata
- Lager scatterplots for visuell vurdering
- Lager regresjonsmodell i scatterplott for visuell vurdering, med usikkerhetslinje
- Lager og trener en lineær regresjonsmodell (sckikit-learn)
- Predikerer fremtidige temperaturer
- Analyse om vi kan nå parisavtalens mål

**Resultater**
- **R2-verdi:** 0.24657103593186125
- **MSE-verdi:** 0.6722834874052438

**Konklusjon**

Vi kan konkludere med at det finnes en sammenheng, men den tydes til å være svak. Det har en forklaringsgrunn til at den lineære regresjonen er forenklet og dataene er hentet fra ulike områder. Likevell er det en tydelig sammenheng og modellen gir en nyttig veiviser for fremtiden.

### Temperaturer og luftkvalitetsnivåer på Elgeseter, Trondheim
**Utførelse:**
- Henter inn, leser og kobler sammen temperaturdata og luftdata
- Lager tre ulike visualiseringer mellom temperatur og NO2, PM10 og PM2.5
- Lager visuell regresjonslinje for hvert stoff

**Resultater**
- **NO2**: Lavere temperaturer gir høyere NO2-konsentrasjoner. Det kan skyldes økt bruk av vedfyring ved kaldere temperaturer og dårligere luftsirkulasjon om vinteren.
- **PM10** og **PM2.5**: Partikkelnivåene synker ved høyere temperaturer. Det kan skyldes at det er mer svevestøv om vinteren, på grunn av piggdekk, veisalting og at den kalde luften ligger nær bakken.

**Konklusjon**

Vi kan konkludere med at lavere temperaturer henger sammen med høyere forurensingsnivåer. Det gir et inntrykk av at kaldt klima forverrer luftkvalitet og gjør at, spesielt i Norge hvor vinteren er lang, luftkvaliteten blir dårligere og dårligere over årene.

### Om R2 og MSE
- **R^2 (R2):** Hvor godt dataene passer sammen kan tallfestes med R^2. Verdien går fra 0 til 1 (eller 0% til 100%), og destro høyere det er, jo bedre.
- **MSE (Mean Squared Error):** Oversatt som midlere kvadratisk feil. Det er en modell som måler hvor store feil en regresjonsmodell kan gjøre. Desto lavere tallet er, desto mer presis er modellen. Det er gjennomsnittet av kvadrerte avvik mellom faktiske og predikerte verdier.


## Visualisering.ipynb
Her visualiseres den analyserte dataen, ved hjelp av Matplotlib, Seaborn, Widgets og Bokeh. Notebooken inneholder ulike typer diagrammer for temperatur, klimagassutslipp og luftkvalitet. 

### Temperatur
For temperaturdata visualiseres utviklingen de siste 50 årene fra Gløshaugen.
Grafene er laget med funksjoner fra temp_visualisering.py, og dataene hentes fra filen temp_gloshaugen_historisk_renset_ 50.csv.
I notatboken er det skrevet refleksjoner og tolkninger i markdown. Det brukes flere ulike graf-typer:

- **Interaktivt linjediagram med Bokeh:**
Viser årlig gjennomsnittstemperatur. Brukeren kan zoome og navigere i grafen, og verdier vises med hover. Varmeste og kaldeste år er også markert.
- **Søylediagram per tiår:**
Viser gjennomsnittstemperatur for hvert tiår og gjør den langsiktige utviklingen tydeligere. Her brukes Matplotlib og Seaborn.
- **Sol-graf:**
En figur som viser total temperaturøkning som en sol. Tallet i midten viser endringen i grader. 

### Klimagassutslipp
For klimagassutslipp visualiseres og analyseres utviklingen i Norge og globalt. Gjennom ulike visualiseringer analyseres endringer over tid og forskjeller mellom sektorer.
Visualiseringene er laget ved hjelp av funksjoner definert i klimagass_visualisering.py, som blir importert via analyser_fil i statistikk.py.
Funksjonene brukes til å generere grafene som presenteres i denne delen av notebooken.

**Konklusjon**

Analysen viser blant annet at Norges klimagassutslipp har gått ned de siste årene, spesielt etter 2020, mens globale utslipp fortsatt å øke. Flere sektorer i Norge, som industri, olje- og gassutvinning og veitrafikk, har redusert sine utslipp over tid.