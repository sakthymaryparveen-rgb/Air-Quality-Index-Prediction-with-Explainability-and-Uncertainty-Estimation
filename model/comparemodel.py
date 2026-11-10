import joblib 
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
import matplotlib.pyplot as plt


df_model= pd.read_pickle("D:/mywork/data/merged_data.pkl")

df_model['Date']=pd.to_datetime(df_model['Date'])

df_model = df_model.sort_values(['Station','Date'])

# Lag features
#weather lags
df_model["wind_roll3"] = df_model.groupby("Station")["wind_speed"].rolling(3).mean().reset_index(0,drop=True)

df_model['temperature_lag1']=df_model.groupby('Station')['temperature'].shift(1)
df_model['wind_speed_lag1']=df_model.groupby('Station')['wind_speed'].shift(1)

#pollutants lags
df_model['PM2.5_lag1']=df_model.groupby('Station')['PM2.5'].shift(1)
df_model['PM10_lag1']=df_model.groupby('Station')['PM10'].shift(1)
df_model['NO2_lag1']=df_model.groupby('Station')['NO2'].shift(1)
df_model['O3_lag1']=df_model.groupby('Station')['O3'].shift(1)

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

features = ['PM2.5_lag1','PM10_lag1','NO2_lag1','O3_lag1',
            'aqi_lag1','aqi_lag3',
            'DayOfYear','roll_std_7',
            'temperature_lag1','wind_speed_lag1','wind_roll3'
]

#split_date='2025-12-01'
train = df_model[df_model['Date'] <'2025-12-01']
test  = df_model[df_model['Date'] >= '2025-12-01']

train=train.dropna()
test=test.dropna()

X_train = train[features]
y_train = train['AQI']

X_test=test[features]
y_test=test['AQI']

print('Total rows:',len(df_model))
print('train rows:',len(train))
print('test rows: ',len(test))

print(X_train.shape)

models = {
    'Linear Regression': LinearRegression(),

    'Decision Tree': DecisionTreeRegressor(
        max_depth=15,
        min_samples_split=4,
        random_state=42
        ),
    
    'Random Forest': RandomForestRegressor(
    n_estimators=600,
    
    max_depth=15,
    min_samples_split=4,
    min_samples_leaf=30,
    
    random_state=42
),
    'Gradient Boosting': GradientBoostingRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=5,
        random_state=42
        ),
    'SVR': SVR(kernel='rbf', C=10, epsilon=0.1)

}
results=[]
for name, model in models.items():
    model.fit(X_train, y_train)
    preds=model.predict(X_test)

    mae=mean_absolute_error(y_test,preds)
    rmse=np.sqrt(mean_squared_error(y_test,preds))
    r2=r2_score(y_test,preds)

    results.append([name, mae, rmse, r2])

    print(f'{name}')
    print(f"MAE: {mae:.3f}")
    print(f"RMSE: {rmse:.3f}")
    print(f"R2: {r2:.3f}")
    print("-"*30)


df_results = pd.DataFrame(results, columns=["Model", "MAE", "RMSE", "R2"])
df_results.sort_values(by="R2", ascending=False)

plt.figure()
plt.bar(df_results["Model"], df_results["R2"])
plt.xticks(rotation=10)
plt.title("Model Comparison (R² Score)")
plt.show()
