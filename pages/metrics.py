import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, r2_score

bundle=joblib.load('D:/mywork/model/rf_bundle.pkl')

model=bundle['model']
features=bundle['features']
mae=bundle['mae']
r2=bundle['r2']
test=bundle['test_data']

st.title("Model Metrics")

col1, col2 = st.columns(2)
col1.metric("MAE", f"{mae:.2f}")
col2.metric("R²", f"{r2:.3f}")

st.subheader('Actual vs Predicted')

fig, ax= plt.subplots()
ax.scatter(test['AQI'],test['aqi_predicted'])
ax.set_xlabel('Actual AQI')
ax.set_ylabel('Predicted AQI')

st.pyplot(fig)

#--------------------------------------------
import numpy as np

all_preds = []

for tree in model.estimators_:
    all_preds.append(tree.predict(test[features]))

all_preds = np.array(all_preds)

mean_pred = all_preds.mean(axis=0)
lower = np.percentile(all_preds, 2.5, axis=0)
upper = np.percentile(all_preds, 97.5, axis=0)

st.subheader('Prediction Interval')

test=test.reset_index(drop=True)

fig2, ax2=plt.subplots()
ax2.plot(test['AQI'].values, label='Actual')
ax2.plot(test['aqi_predicted'], label='Predicted')

ax2.fill_between(
    range(len(lower)),
    lower,upper,alpha=0.3)

ax2.legend()
st.pyplot(fig2)

#-----------------------------------------------
importances=model.feature_importances_
st.subheader('Feature Importance')

fig3,ax3=plt.subplots(figsize=(8,5))

feature_df=pd.DataFrame({
    'Feature':features,
    'Importance':importances
})

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
feature_df['Feature'] = feature_df['Feature'].str.strip()
feature_df['Feature']=feature_df['Feature'].map(feature_map).fillna(feature_df['Feature'])
#feature_df=feature_df.sort_values('Importance',ascending=False)

ax3.bar(feature_df['Feature'],feature_df['Importance'])
ax3.set_xticklabels(features,rotation=45,ha='right')
ax3.set_ylabel('Importance')
ax3.set_xlabel('Features')

st.pyplot(fig3)

st.divider()
