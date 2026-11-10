import pandas as pd

import matplotlib.pyplot as plt

#ata=pd.read_csv("chennai_clean_ready_for_aqi.csv")
def handle_missing(data):
    data['Date']=pd.to_datetime(data['Date'])

    missing=data.isna().sum()
    #print(missing[missing>0])
    #print(data.isna().mean()*100)

    data=data.sort_values(['Date','Station'])
    data=data.set_index('Date')
    cols=['CO','NO2','SO2','O3','PM10','PM2.5']

    data[cols]=data.groupby('Station')[cols].transform(
        lambda x:x.interpolate(method='time',limit_direction='both')
    )
    #print(data.isna().sum())
    #print(data.groupby('Station').size())
    data=data.reset_index()

    '''plt.figure(figsize=(15,4))
    sns.heatmap(data[['CO','NO2','SO2','O3','PM10','PM2.5']].isna().T,cmap=['green','red'],cbar=False)
    plt.title('Green=Present,Red- Missing')
    plt.xlabel('Date Index')
    plt.show()'''

    #data=data.rename(columns={'PM2.5':'PM25'})

    #data.to_csv("handled_missing.csv", index=False)
    return data
    #print('file saved')