import pandas as pd
import numpy as np

# Hjelpefunksjoner

# Renser kolonnenavn: små bokstaver, ingen mellomrom, spesialtegn fjernes
def rens_kolonnenavn(df):
    df.columns = df.columns.str.strip().str.replace('"', '').str.lower()
    df.columns = df.columns.str.replace(" ", "_").str.replace("µg/m³", "ugm3").str.replace("ug/m3", "ugm3")
    return df

#  Legger til tidsegenskaper: år, måned, dato og time hvis mulig

def legg_til_tid(df, tidkolonne="tid", groupby=None):

    if tidkolonne not in df.columns:
        return df

    # Hvis det er heltall ( bare årstall)
    if pd.api.types.is_integer_dtype(df[tidkolonne]):
        df['år'] = df[tidkolonne]
    else:
        df[tidkolonne] = pd.to_datetime(df[tidkolonne], errors='coerce')
        df['dato'] = df[tidkolonne].dt.date
        df['år'] = df[tidkolonne].dt.year
        df['måned'] = df[tidkolonne].dt.month
        df['time'] = df[tidkolonne].dt.hour

    # hopper over måned og time hvis det kun er år i anlysen
    if groupby == 'år':
        df = df.drop(columns=['måned', 'time'], errors='ignore')

    return df


# Finne kolonne som inneholder 'kilde'
def finn_kildekolonne(df):
    kildekolonner = [kol for kol in df.columns if "kilde" in kol]
    return kildekolonner[0] if kildekolonner else None

# Analysefunksjoner

# Leser inn og analyserer en CSV-fil, returnerer statistikk, totaldata og ryddet df
def analyser_fil(filsti, sep=',', datokolonne=None, groupby='måned'):
    df = pd.read_csv(filsti, sep=sep)
    df = rens_kolonnenavn(df)

    if not datokolonne:
        return None, None, df

    datokolonne = datokolonne.strip().lower()
    if datokolonne not in df.columns:
        return None, None, df

    df = legg_til_tid(df, datokolonne, groupby)

    kildekol = finn_kildekolonne(df)
    df_total = None

    if kildekol and kildekol in df.columns:
        df_total = df[df[kildekol].astype(str).str.lower().str.contains("alle kilder")].copy()
        df[kildekol] = df[kildekol].astype(str).str.strip()
        df = df[~df[kildekol].str.lower().str.contains("alle kilder")].copy()

    grupper = ['år']
    if groupby == 'måned':
        grupper.append('måned')
    if kildekol and kildekol in df.columns:
        grupper.insert(0, kildekol)

    if not grupper:
        return None, None, df

    numeriske_kolonner = df.select_dtypes(include=[np.number]).columns.difference(['år', 'måned'])
    numeriske_kolonner = [kol for kol in numeriske_kolonner if not kol.lower().startswith("dekning")]

    statistikk = {}

    for kol in numeriske_kolonner:
        gruppe_størrelser = df.groupby(grupper).size()

        if gruppe_størrelser.min() > 1:
            stats = df.groupby(grupper)[kol].agg(['mean', 'median', 'std']).reset_index()
        else:
            stats = df.groupby(grupper)[kol].agg(['mean', 'median']).reset_index()

        stats = stats.rename(columns={
            'mean': 'gjennomsnitt',
            'median': 'median',
            'std': 'standardavvik'
        })
        statistikk[kol] = stats

    return statistikk, df_total, df


# Analyserer temperaturdata
def analyser_temperatur(filsti, datokolonne="tidspunkt", groupby="måned"):

    statistikk_temp, df_total, df = analyser_fil(filsti, datokolonne=datokolonne, groupby=groupby)

    resultat = {}

    for navn, df in statistikk_temp.items():
        samlet_statistikk = df.round(2)

        årlig_snitt = None
        if 'år' in df.columns and 'måned' in df.columns:
            antall_mnd = df.groupby('år')['måned'].count().reset_index(name='antall_måneder')
            hele_år = antall_mnd[antall_mnd['antall_måneder'] == 12]['år']

            df_hele_år = df[df['år'].isin(hele_år)]
            årlig_snitt = df_hele_år.groupby('år')['gjennomsnitt'].mean().reset_index(name='årsgjennomsnitt').round(2)

        resultat[navn] = {
            "samlet_statistikk": samlet_statistikk,
            "årlig_snitt": årlig_snitt
        }

    return resultat

# Beregner absolutt og prosentvis endring mellom første og siste år
def beregn_endring_totalt(df, årskolonne='år', verdikolonne='årsgjennomsnitt'):
    df = df.copy()
    første = df.iloc[0]
    siste = df.iloc[-1]

    endring = siste[verdikolonne] - første[verdikolonne]
    prosent = (endring / abs(første[verdikolonne])) * 100

    return {
        "startår": int(første[årskolonne]),
        "sluttår": int(siste[årskolonne]),
        "endring": endring,
        "prosent": prosent
    }

# Beregner årlig absolutt og prosentvis endring
def beregn_endring_årlig(df, årskolonne='år', verdikolonne='årsgjennomsnitt'):
    df = df.copy()
    df['absolutt_endring'] = df[verdikolonne].diff()
    df['prosent_endring'] = df[verdikolonne].pct_change() * 100
    return df[[årskolonne, verdikolonne, 'absolutt_endring', 'prosent_endring']]

 # Finner året med høyest og lavest verdi
def ekstremverdier(df, årskolonne='år', verdikolonne='gjennomsnitt'):
    df = df.copy()
    år_maks = df.loc[df[verdikolonne].idxmax()]
    år_min = df.loc[df[verdikolonne].idxmin()]

    return {
        "maksimum": {
            "år": int(år_maks[årskolonne]),
            "verdi": år_maks[verdikolonne]
        },
        "minimum": {
            "år": int(år_min[årskolonne]),
            "verdi": år_min[verdikolonne]
        }
    }

# Beregner gjennomsnitt per tiår
def tiår_snitt(df, årskolonne='år', verdikolonne='gjennomsnitt'):
    df = df.copy()
    df['tiår'] = (df[årskolonne] // 10) * 10
    tiår_snitt = df.groupby('tiår')[verdikolonne].mean().reset_index()
    tiår_snitt[verdikolonne] = tiår_snitt[verdikolonne].round(2)
    return tiår_snitt

# Beregner avvik fra totalgjennomsnitt
def beregn_avvik(df, årskolonne='år', verdikolonne='årsgjennomsnitt'):
    df = df.copy()
    total_snitt = df[verdikolonne].mean()
    df['avvik'] = df[verdikolonne] - total_snitt
    return df[[årskolonne, verdikolonne, 'avvik']]

#  Analyserer utslipp i Norge per kilde og år
def analyser_utslipp_norge(df, årskolonne='år', kildekolonne='kilde_(aktivitet)'):
    df = df.copy()
    kol_utslipp = [kol for kol in df.columns if 'utslipp' in kol.lower() and 'co2' in kol.lower()]
    if not kol_utslipp:
        return None
    kol_utslipp = kol_utslipp[0]

    df[kol_utslipp] = pd.to_numeric(df[kol_utslipp], errors="coerce")

    if kildekolonne in df.columns:
        df = df[~df[kildekolonne].str.contains("alle kilder", case=False, na=False)]

    if not df.empty and årskolonne in df.columns and kildekolonne in df.columns:
        stats_per_kilde_år = df.groupby([kildekolonne, årskolonne])[kol_utslipp].agg(['mean', 'median']).reset_index()
        return stats_per_kilde_år.round(2)
    else:
        return None

 # Beregner gjennomsnitt og median for hver kilde 
def gjennomsnitt_per_kilde(df, kildekolonne='kilde_(aktivitet)', årskolonne='år'):
    df = df.copy()
    kol_utslipp = [kol for kol in df.columns if 'utslipp' in kol.lower() and 'co2' in kol.lower()]
    if not kol_utslipp:
        return None
    kol_utslipp = kol_utslipp[0]

    df[kol_utslipp] = pd.to_numeric(df[kol_utslipp], errors="coerce")

    if not df.empty and kildekolonne in df.columns:
        stats_per_kilde = df.groupby(kildekolonne)[kol_utslipp].agg(['mean', 'median']).round(2)
        return stats_per_kilde.sort_values(by='mean', ascending=False)
    else:
        return None

# Lager en datastruktur med år og totalutslipp
def lag_totaldata(df_total, årskolonne='år'):
    df_total = df_total.copy()
    kol_utslipp = [kol for kol in df_total.columns if 'utslipp' in kol.lower() and 'co2' in kol.lower()]
    kol_utslipp = kol_utslipp[0]

    total = df_total[[årskolonne, kol_utslipp]].copy()
    total = total.rename(columns={kol_utslipp: 'utslipp'})
    return total.sort_values(by=årskolonne)

 # Beregner årlige endringer i utslipp per kilde 
def beregn_endring_per_kilde(df, aktivitetskolonne='kilde_(aktivitet)', årskolonne='år', verdikolonne='mean'):
    resultater = {}

    for kilde in df[aktivitetskolonne].unique():
        df_kilde = df[df[aktivitetskolonne] == kilde].copy()
        df_kilde = df_kilde.sort_values(årskolonne)

        df_kilde_endring = beregn_endring_årlig(df_kilde, verdikolonne=verdikolonne)
        resultater[kilde] = df_kilde_endring

    return resultater

# Analyserer luftkvalitetsdata for ulike stoffer
def analyser_luftkvalitet(df_luft, målinger):
    resultater = {}

    for stoff in målinger:
        stoff_resultat = {}

        daglig = df_luft.groupby("dato")[stoff].mean().reset_index(name="daglig_snitt")
        stoff_resultat["daglig"] = daglig

        årlig = df_luft.groupby("år")[stoff].mean().reset_index(name="årssnitt")
        stoff_resultat["årlig"] = årlig

        månedlig = df_luft.groupby("måned")[stoff].mean().reset_index(name="månedsnitt")
        stoff_resultat["månedlig"] = månedlig

        rush = df_luft.groupby("time")[stoff].mean().reset_index(name="snitt_per_klokkeslett")
        stoff_resultat["rush"] = rush

        stoff_resultat["ekstremer"] = ekstremverdier(df_luft, verdikolonne=stoff)

        resultater[stoff] = stoff_resultat

    return resultater
