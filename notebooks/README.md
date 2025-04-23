## Dataanalyse av miljødata
I notebooken vises det hvordan vi bruker funksjonene i `dataanalyse.py` til å analysere de rensede datasettene: 

- Temperaturdata (`temp_gloshaugen_historisk.csv`)
- Klimagassutslipp (`klimagassutslipp_renset.csv`)
- Luftkvalitet (`luftkvalitet.json`)

### Det som gjøres i notebooken:
- Importerer funksjoner fra `src/dataanalyse.py`
- Kjører `analyser_fil()` på hvert datasett
- Bruker `json_til_dataframe()` for å konvertere JSON til CSV
- Grupperer data etter år og/eller måned

For å vise resultatet på en oversiktlig måte i notebooken brukes en løkke og display() slik at DataFrame blir vist på en pen måte  i Jupyter. 


## Prediktiv_analyse
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

## Visualisering
PS: VISUALISERINGEN ER IKKE FERDIG
Her visualiseres den analyserte dataen, ved hjelp av Matplotlib, Seaborn, Widgets og Bokeh. Notebooken inneholder ulike typer diagrammer for temperatur, klimagassutslipp og luftkvalitet. 

### Temperatur
#### Linjediagram
Her brukes Bokeh til å lage et linjediagram som viser utviklingen av gjennomsnittstemperaturen de siste 50 årene. Dette er et interaktivt diagram der man kan zoome og flytte på diagrammet. I tillegg brukes hover så brukeren enkelt kan se verdien på hvert datapunkt. Høyeste og laveste verdi som ble funnet i analysen er også markert for å gjøre diagrammet mer informativt.
#### Søylediagram
Søylediagrammet viser gjennomsnittstemperaturen per tiår, som gir et mer tydelig bilde på den generelle temperaturøkningen. Til visualiseringen brukes Matplotlib og Seaborn.

### Klimagassutslipp


### Luftkvalitet
#### Linjediagram
Dette skal utbedres
