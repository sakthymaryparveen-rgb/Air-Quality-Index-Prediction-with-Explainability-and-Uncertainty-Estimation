from data.aqi_breakpoints import (
    pm10_sub_index, pm25_sub_index,
    no2_sub_index, so2_sub_index,
    o3_sub_index, co_sub_index
)

import pandas as pd
import numpy as np


def computation(df):
    #df = pd.read_csv('data/chennai_clean_ready_for_aqi.csv')

    df['pm25_sub'] = df['PM2.5'].apply(pm25_sub_index)
    df['pm10_sub'] = df['PM10'].apply(pm10_sub_index)
    df['no2_sub']  = df['NO2'].apply(no2_sub_index)
    df['so2_sub']  = df['SO2'].apply(so2_sub_index)
    df['o3_sub']   = df['O3'].apply(o3_sub_index)
    df['co_sub']   = df['CO'].apply(co_sub_index)

    sub_cols = ['pm25_sub','pm10_sub','no2_sub','so2_sub','o3_sub','co_sub']

# Minimum 3 pollutant rule
    valid_counts = df[sub_cols].notna().sum(axis=1)

    pm_condition=df[['pm25_sub','pm10_sub']].notna().any(axis=1)
    valid_mask=(valid_counts >=3) & pm_condition

    df['AQI'] = np.where(
    valid_counts ,
    df[sub_cols].max(axis=1).round(),
    np.nan
    )

    df['Dominant_Pollutant'] = (
    df[sub_cols]
    .idxmax(axis=1)
    .str.replace('_sub','')
    )

    def aqi_category(x):
        if pd.isna(x):
            return None
        if x <= 50:
            return 'Good'
        elif x <= 100:
            return 'Satisfactory'
        elif x <= 200:
            return 'Moderate'
        elif x <= 300:
            return 'Poor'
        elif x <= 400:
            return 'Very Poor'
        else:
            return 'Severe'

    df['AQI_Category'] = df['AQI'].apply(aqi_category)

    return df
'''df.to_csv('chennai_pollutants_with_aqi.csv', index=False)
print('File Saved')'''