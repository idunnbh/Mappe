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
Denne notebooken tar for seg en predektiv analyse med lineær regresjon. Her undersøker vi om det finnes en sammenheng mellom luftkvalitet og temperatur, og hvorvidt det er mulig å bruke luftkvalitetsmålinger til å prediktere temperaturer.

### Datagrunnlag
- **Temperaturdata:** Data er hentet fra data/temp_gloshaugen_historisk_renset.csv
- **Luftkvalitetsdata:** Data er hentet fra data/hitorisk_luftkvalitet.csv

### Innhold - Hva gjør notebooken?
- Leser inn og slår sammen temperatur- og luftkvalitetsdta
- Lager scatterplots for visuell vurdering
- Trener to lineære regresjonsmodeller
  - Én med NO2, PM10 og PM2.5
  - Én med kun NO2
- Evaluerer modellene
- Visualiserer faktisk vs. predikert temperatur
- Sammenligner modellene og vurderer om luftkvalitet forklarer temperatur

### Resultater
- R2-verdi med NO2, PM10 og PM2.5: **0.054**
- R2-verdi med kun NO2: **0.025**
- Resultatene og visualiseringene viser at luftkvalitet alene ikke forklarer variasjon i temperatur i noen grad.

### Konklusjon
Regresjonsmodellene har lav forklaringskraft og det ser ikke ut til at vurderingsvariablene NO2, PM10 og PM2.5 kan kanb brukes alene for å forutsi temperatur. Andre miljøfaktorer bør vurderes om man ønsker å analysere videre.

Denne notebooken viser likevel et godt eksempel på hvordan prediktiv analyse kan brukes til å teste hypoteser i miljødata, tross for at den lineære regresjonen ikke var vellykket.

### Om R2 og MSE
- **R^2 (R2):** Hvor godt dataened passer sammen kan tallfestes med R^2. Verdien går fra 0 til 1, og destro høyere det er, jo bedre. I denne analysen forteller R2-verdien om hvor mye av variasjonen i temperaturer modellen klarer å forklare. En R2 på 0.054 betyr at de har en forklaringsgrad på 5%, som er relativt lite.
- **MSE (Mean Squared Error):** Oversatt som midlere kvadratisk feil. Det er en modell som måler hvor store feil en regresjonsmodell kan gjøre. Desto lavere tallet er, desto mer presis er modellen. Det er gjennomsnittet av kvadrerte avvik mellom faktiske og predikerte verdier.