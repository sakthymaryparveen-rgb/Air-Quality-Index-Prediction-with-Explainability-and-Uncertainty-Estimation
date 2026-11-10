import os
import joblib
import streamlit as st
import numpy as np
import pandas as pd
from datetime import timedelta
import shap

model=joblib.load("D:/mywork/model/rf_aqi_model.pkl")

# Attempt to load data saved by the Upload Data page
data_path = "D:/mywork/data/model_data.pkl"
if not os.path.exists(data_path):
    st.info('Please go to the "Upload File" page to prepare your data first.')
    st.stop()
    
try:
    df = pd.read_pickle(data_path)
except Exception as e:
    st.error(f"Error loading prepared dataset: {e}")
    st.stop()


explainer=shap.TreeExplainer(model)

df=df[['Date','Station','AQI','PM2.5','PM10','NO2','O3','SO2','CO']]

df=df.sort_values(['Station','Date'])

st.title('AQI Prediction with Uncertainty')

station=st.selectbox('Station',df['Station'].unique())
df_station=df[df['Station']==station].copy()


if st.button('Predict Tomorrow AQI'):

    if len(df_station) < 7:
        st.warning('Not enough data') # not enough history
    else:
        last_row = df_station.iloc[-1]
        tomorrow = last_row["Date"] + timedelta(days=1)

        new_row = pd.DataFrame({
            "PM2.5_lag1": [last_row["PM2.5"]],
            "PM10_lag1": [last_row["PM10"]],
            "NO2_lag1": [last_row["NO2"]],
            "O3_lag1": [last_row["O3"]],
            "SO2_lag1": [last_row["SO2"]],
            "CO_lag1":[last_row["CO"]],
            "aqi_lag1": [last_row["AQI"]],
            "aqi_lag3": [df_station.iloc[-3]["AQI"]],
            "aqi_lag7": [df_station.iloc[-7]["AQI"]],
            "roll_mean_3": [df_station["AQI"].iloc[-3:].mean()],
            "DayOfYear": [tomorrow.timetuple().tm_yday]
        })

    # Uncertainty from trees
        tree_preds = np.array([
            tree.predict(new_row.values)
            for tree in model.estimators_
        ])

        mean_pred = np.mean(tree_preds)
        lower = np.percentile(tree_preds, 2.5)
        upper = np.percentile(tree_preds, 97.5)

        st.subheader(f'Prediction for {tomorrow.date()}')
        st.metric('Predicted AQI',round(mean_pred,2))
        st.write(f'Expected Range: {round(lower,2)} - {round(upper,2)}')
        


        #shap
        shap_values = explainer.shap_values(new_row)

        feature_map={
            'aqi_lag1': 'Yesterday AQI',
        'aqi_lag3': 'AQI 3 days ago',
        'DayOfYear': 'Seasonal effect (time of year)',
        'NO2_lag1': 'Yesterday NO2 level',
        'temperature_lag1': 'Yesterday temperature',
        'PM2.5_lag1': 'Yesterday PM2.5 level',
        'wind_speed_lag1': 'Yesterday wind speed',
        'PM10_lag1': 'Yesterday PM10 level',
        'O3_lag1': 'Yesterday Ozone (O3)',
        'wind_roll3': '3-day average wind speed',
        'roll_std_7': 'Pollution variability (last 7 days)'
        }

        explain_df=pd.DataFrame({
            'Feature':new_row.columns,
            'Impact':shap_values[0]})
        
        explain_df['Feature']=explain_df['Feature'].map(feature_map).fillna(explain_df['Feature'])

        explain_df['AbsImpact']=explain_df['Impact'].abs()
        explain_df=explain_df.sort_values('AbsImpact',ascending=False)
        explain_df=explain_df.head(8)

        st.subheader('Feature Contribution')
        st.dataframe(
            explain_df[['Feature','Impact']])

        st.bar_chart(
            explain_df.set_index('Feature')['Impact'])
