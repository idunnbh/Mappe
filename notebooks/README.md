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
