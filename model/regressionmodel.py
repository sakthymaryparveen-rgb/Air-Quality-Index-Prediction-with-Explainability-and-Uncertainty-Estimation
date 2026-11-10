'''import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','data')))
from aqi_computation import computation'''
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import joblib

#df_model=computation('handled_missing.csv')
df_model=joblib.load('D:/mywork/data/model_data.pkl')
df_model['Date']=pd.to_datetime(df_model['Date'])

df_model = df_model.sort_values(['Station','Date'])

#pollutants lags
df_model['PM25_lag1']=df_model.groupby('Station')['PM2.5'].shift(1)
df_model['PM10_lag1']=df_model.groupby('Station')['PM10'].shift(1)
df_model['NO2_lag1']=df_model.groupby('Station')['NO2'].shift(1)
df_model['SO2_lag1']=df_model.groupby('Station')['SO2'].shift(1)
df_model['O3_lag1']=df_model.groupby('Station')['O3'].shift(1)
df_model['CO_lag1']=df_model.groupby('Station')['CO'].shift(1)

df_model['aqi_lag1']=df_model.groupby('Station')['AQI'].shift(1)
df_model['aqi_lag3']=df_model.groupby('Station')['AQI'].shift(3)
df_model['aqi_lag7']=df_model.groupby('Station')['AQI'].shift(7)

# Rolling features (no leakage)
df_model['roll_mean_3'] = (
    df_model.groupby('Station')['AQI']
    .shift(1)
    .rolling(3)
    .mean()
    .reset_index(0, drop=True)
)

df_model['roll_std_7'] = (
    df_model.groupby('Station')['AQI']
    .shift(1)
    .rolling(7)
    .std()
    .reset_index(0, drop=True)
)

df_model['Month'] = df_model['Date'].dt.month

df_model['DayOfYear'] = df_model['Date'].dt.dayofyear

#df=pd.merge(df_model,weather,on=['Date','Station'],how='inner')

features = ['PM25_lag1','PM10_lag1','NO2_lag1','O3_lag1','SO2_lag1','CO_lag1',
            'aqi_lag1','aqi_lag3','aqi_lag7','roll_mean_3',
            'DayOfYear'
]

#split_date='2025-12-01'
train = df_model[df_model['Date'] <'2026-01-01']
test  = df_model[df_model['Date'] >= '2026-01-01']

train=train.dropna()
test=test.dropna()

X_train = train[features]
y_train = train['AQI']

print('Total rows:',len(df_model))
print('train rows:',len(train))
print('test rows: ',len(test))

print(X_train.shape)

model = RandomForestRegressor(
    n_estimators=600,
    criterion='squared_error',
    max_depth=15,
    min_samples_split=4,
    min_samples_leaf=30,
    
    random_state=42
)

model.fit(X_train, y_train)

for name, imp in zip(X_train.columns, model.feature_importances_):
    print(name, round(imp,3))

test=test.copy()
test.loc[:,'aqi_predicted'] = model.predict(test[features])

validation = pd.merge(
    test[['Date','Station','aqi_predicted']],
    test[['Date','Station','AQI']],
    on=['Date','Station'],
    how='inner'
)

mae = mean_absolute_error(validation['AQI'], validation['aqi_predicted'])
r2  = r2_score(validation['AQI'], validation['aqi_predicted'])

print("MAE:", mae)
print("R2:", r2)

import joblib

bundle = {
    "model": model,
    "features": features,
    "mae": mae,
    "r2": r2,
    "test_data":test
}

joblib.dump(bundle, "D:/mywork/model/rf_bundle.pkl")

joblib.dump(model,'D:/mywork/model/rf_aqi_model.pkl')
