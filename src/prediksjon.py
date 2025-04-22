import pandas as pd

def prediksjon1(temp_les, luftkvalitet_les):
    temp = pd.read_csv(temp_les)
    temp["tidspunkt"] = pd.to_datetime(temp["tidspunkt"])
    temp["tidspunkt"] = temp["tidspunkt"].dt.tz_localize(None)

    luft = pd.read_csv(luftkvalitet_les)
    luft.columns = luft.columns.str.strip()
    luft["Tid"] = pd.to_datetime(luft["Tid"], dayfirst=True)

    luft = luft.rename(columns={
        "Elgeseter NO2 µg/m³ Hour": "NO2",
        "Elgeseter PM10 µg/m³ Hour": "PM10",
        "Elgeseter PM2.5 µg/m³ Hour": "PM25"
    })

    # Merge
    df = pd.merge(temp, luft, left_on="tidspunkt", right_on="Tid")
    df = df[["tidspunkt", "temperatur", "NO2", "PM10", "PM25"]]
    df = df.dropna()

    return df
