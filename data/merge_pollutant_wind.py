import pandas as pd

pollutant=pd.read_csv('data/chennai_pollutants_with_aqi.csv')
weather=pd.read_csv('data/clean_weather_data.csv')

col1=['Date','Station','CO','NO2','SO2','O3','PM10','PM2.5','AQI','Dominant_Pollutant','AQI_Category']
pollutant=pollutant[col1]

df=pd.merge(pollutant,weather,on=['Date','Station'],how='inner')

df.to_csv('final_model_dataset.csv')
print('File Saved')