import pandas as pd
import streamlit as st
import altair as alt
import joblib

st.title('Chennai Air Pollutants Analysis')
st.sidebar.title('Air Quality Data Visualization')

df=joblib.load('D:\mywork\data\merged_data.pkl')

df['Date']=pd.to_datetime(df['Date'])
df=df.rename(columns={'PM2.5': 'PM25'})
cols=['PM10','PM25','NO2','SO2','CO','O3','AQI']
df[cols]=df[cols].apply(pd.to_numeric, errors='coerce')

station=st.selectbox('Station',df['Station'].unique())

filtered_df=df[df['Station']==station].sort_values('Date')

aqi_chart=alt.Chart(filtered_df).mark_line(color='blue').encode(
    x='Date:T',
    y='AQI:Q',
    tooltip=['Date','AQI']
).properties(title='AQI trend over time')

pm25_chart=alt.Chart(filtered_df).mark_line(color='red').encode(
    x='Date:T',
    y='PM25:Q',
    tooltip=['Date','PM25']
).properties(title='PM2.5 trend over time')

pm10_chart=alt.Chart(filtered_df).mark_line(color='green').encode(
    x='Date:T',
    y='PM10:Q',
    tooltip=['Date','PM10']
).properties(title='PM10 trend over time')

multi_df=filtered_df.melt(
    id_vars=['Date'],
    value_vars=['NO2','SO2','CO','O3'],
    var_name='Pollutant',
    value_name='Value'
).dropna()

multi_chart=alt.Chart(multi_df).mark_line().encode(
    x='Date:T',
    y='Value:Q',
    color='Pollutant:N',
    tooltip=['Date','Pollutant','Value']
).properties(title='Gas pollutants trend over time')

#display
st.altair_chart(aqi_chart,use_container_width=True)

col1, col2=st.columns(2)

with col1:
    st.altair_chart(pm25_chart,use_container_width=True)

with col2:
    st.altair_chart(pm10_chart,use_container_width=True)

st.altair_chart(multi_chart,use_container_width=True)
