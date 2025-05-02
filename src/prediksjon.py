import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def koble_temp_klima(df_klima, df_temp):
    df_temp["år"] = df_temp["tidspunkt"].dt.year
    df_temp_agg = df_temp.groupby("år")["temperatur"].mean().reset_index()
    df_merged = pd.merge(df_temp_agg, df_klima, left_on="år", right_on="År").drop(columns=["År"])

    return df_merged, df_temp_agg