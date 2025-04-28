# Analyse av temperatur, klimagassutslipp og luftkvalitet

Dette prosjektet analyserer temperatur, klimagassutslipp og luftkvalitet i Norge/Trondheim, for å finne sammenhenger mellom klimaendringer, miljø og helse.
Prosjektet kombinerer flere datasett for å identifisere trender og potensielle konsekvenser.

## Innhold

- [Datasett](#datasett)
- [Mål for prosjektet](#mål-for-prosjektet)
- [Filstruktur](#filstruktur)
- [Kilder](#kilder)

## Datasett

- **Temperaturdata:** Meteorologisk institutt (MET API og Frost API)
- **Klimagassutslipp Norge:** Statistisk sentralbyrå (SSB)
- **Klimagassutslipp verden:** Our World in Data (OWID)
- **Luftkvalitet:** Norsk institutt for luftforskning (NILU) og sanntidsdata fra MET


## Mål for prosjektet
Målet med prosjektet er å finne sammenhenger og analysere data for temperatur, klimagassutslipp og luftkvalitet i Norge/Tronheim for å finne sammenhenger mellom dem. Dette er for å forstå hvordan klimaendringer kan påvirke miljø og helse.

Spesielt ønsker vi studere:
- Hvordan økte utslipp av klimagasser henger sammen med temperaturendringer.
- Hvordan temperaturendringer igjen kan påvirke luftkvaliteten.
- Trender for å forstå langsiktige konsekvenser.

Ved å kombinere disse datasettene håper vi å finne trender som kan gi større forståelse i de langsiktige konsekvensene av klimaendringer på lokalt nivå.


## Filstruktur
Prosjektet er strukturert slik:

├── data/           # Rådata og rensede datafiler
├── notebooks/      # Jupyter Notebooks (analyser, visualisering)
├── src/            # Kildekode (datainnsamling, rensing, analyse)
├── tests/          # Enhetstester
├── README.md       # (Denne filen)

## Kilder

1) [Meteorologisk institutt - Locationforecast API v2](https://api.met.no/weatherapi/locationforecast/2.0/documentation)  
2) [Meteorologisk institutt - Frost API](https://frost.met.no/)  
3) [Statistisk sentralbyrå (SSB) - Utslipp av klimagasser](https://www.ssb.no/statbank/table/13931)  
4) [Our World in Data - CO₂ and Greenhouse Gas Emissions](https://ourworldindata.org/co2-and-greenhouse-gas-emissions#all-charts)  
5) [Norsk institutt for luftforskning (NILU)](https://www.nilu.no/)  
6) [Meteorologisk institutt (MET)](https://api.met.no/)
