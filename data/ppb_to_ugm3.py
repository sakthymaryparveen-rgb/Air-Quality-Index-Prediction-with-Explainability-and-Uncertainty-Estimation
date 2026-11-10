import pandas as pd
import numpy as np

#data=pd.read_csv("chennai_aqi_2025_stations.csv")

def conversion(df):

# Rename column
    df = df.rename(columns={"O3 MASS": "O3"})

# Convert pollutants to numeric safely
    pollutants = ["CO","NO2","SO2","O3","PM10","PM2.5"]
    for col in pollutants:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# -------------------------
# Convert ppb → mass units
# -------------------------
    MW = {"CO":28.01, "NO2":46.01, "SO2":64.07}

    mask = df["Units"] == "ppb"

    for gas, mw in MW.items():
        df.loc[mask, gas] = ((df.loc[mask, gas] * mw) / 24.45).round(3)

# Convert CO to mg/m³ (CPCB uses mg/m³)
    #df.loc[mask, "CO"] = df.loc[mask, "CO"] / 1000

# -------------------------
# Merge split rows
# -------------------------
    df_combined = (
        df.groupby(["Date","Station","Location_ID"], as_index=False)
        .agg({
          "CO":"max",
          "NO2":"max",
          "SO2":"max",
          "O3":"max",
          "PM10":"max",
          "PM2.5":"max"
      })
)

# -------------------------
# Remove negatives
# -------------------------
    for col in pollutants:
        df_combined.loc[df_combined[col]<0,col]=np.nan

# -------------------------
# Remove unrealistic values
# -------------------------
    df_combined.loc[df_combined["CO"] > 10, "CO"] = np.nan
    df_combined.loc[df_combined["NO2"] > 1000, "NO2"] = np.nan
    df_combined.loc[df_combined["SO2"] > 1000, "SO2"] = np.nan
    df_combined.loc[df_combined["PM10"] > 2000, "PM10"] = np.nan
    df_combined.loc[df_combined["PM2.5"] > 1000, "PM2.5"] = np.nan
    df_combined.loc[df_combined["O3"] > 500, "O3"] = np.nan

    for col in ["PM10","PM2.5","NO2","SO2","O3"]:
        upper = df_combined[col].quantile(0.995)
        df_combined.loc[df_combined[col] > upper, col] = upper

    
# -------------------------
# Save clean file
# -------------------------


    df_combined['Date']=pd.to_datetime(df_combined['Date'])
    stations=df_combined['Station'].unique()
    full_dates=pd.date_range(df_combined['Date'].min(),df_combined['Date'].max(),freq='D')

    idx=pd.MultiIndex.from_product([stations,full_dates],names=['Station','Date'])
    df_combined=df_combined.set_index(['Station','Date']).reindex(idx).reset_index()

    drop=['Arumbakkam, Chennai - TNPCB']
    df_combined=df_combined[~df_combined["Station"].isin(drop)]

    df_combined['Location_ID']=df_combined['Location_ID'].ffill()

    #df_combined.to_csv("chennai_clean_ready_for_aqi.csv", index=False)
    #print('file saved')
    return df_combined
'''
# Quick check
print(df_combined[['CO','NO2','SO2']].describe(percentiles=[0.95, 0.99]))
print(df_combined[["PM2.5",'PM10','O3']].describe(percentiles=[0.95, 0.99]))

print("Clean merged file saved.")
'''
