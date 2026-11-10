# 🌫️ AQI Prediction with Explainability and Uncertainty Estimation

An interactive air quality forecasting application built using **Machine Learning, Explainable AI (XAI), and Streamlit**. The system predicts next-day Air Quality Index (AQI) using historical pollutant observations and provides prediction uncertainty estimates and SHAP-based explanations.

## 📌 Project Overview

Air pollution is an increasing environmental concern. Predicting future air quality can help people better understand potential pollution levels and make informed decisions.

This project develops an interactive machine learning application to forecast the next day's AQI using historical pollutant concentration data.

The system combines:
- Random Forest regression for next-day AQI forecasting.
- SHAP for explaining individual model predictions.
- Tree-based percentile estimation for communicating prediction uncertainty.
- Interactive pollutant visualization through historical line charts.
- Streamlit for presenting predictions, explanations, and model evaluation.

Currently, the project covers monitoring stations in **Chennai, Tamil Nadu, India**, with plans to expand to multiple districts.

## ✨ Key Features

- **Next-Day AQI Forecasting:** Predicts the next day's AQI using a Random Forest Regressor.
- **Real-World Pollutant Data:** Uses pollutant observations collected from OpenAQ.
- **Data Preprocessing:** Includes pollutant unit conversion and missing-value handling using interpolation.
- **CPCB-Based AQI Calculation:** Calculates AQI values using the Central Pollution Control Board methodology.
- **Explainable AI:** Uses SHAP TreeExplainer to understand feature contributions to predictions.
- **Uncertainty Estimation:** Estimates lower and upper prediction values using the 2.5th and 97.5th percentiles of individual decision tree predictions.
- **Pollutant Visualization:** Displays historical pollutant trends using interactive line charts.
- **Model Evaluation:** Presents regression performance metrics through the Streamlit interface.
- **Interactive Application:** Provides a user-friendly interface for pollutant inputs, AQI predictions, and model interpretation.

## 📊 Dataset

Historical pollutant concentration data was collected from the OpenAQ platform.

| Attribute | Details |
|-----------|---------|
| Data source | OpenAQ |
| Geographic coverage | Chennai, Tamil Nadu, India |
| Data collection period | February 2025 – January 2026 |
| Data type | Historical pollutant observations |
| Target variable | Air Quality Index (AQI) |

### Data Preprocessing

The following preprocessing steps were performed:

1. Collected historical pollutant observations from OpenAQ.
2. Converted pollutant concentrations into the required measurement units.
3. Identified and handled missing pollutant values using interpolation.
4. Calculated AQI values using the standard CPCB methodology.
5. Prepared the processed dataset for machine learning model development.

## ⚙️ Methodology

### 1. AQI Calculation

After pollutant preprocessing and missing-value handling, AQI values were calculated using the CPCB methodology.

These calculated AQI values were used as the target variable for machine learning model development.

### 2. Feature Engineering

Lag-based features were created to capture historical pollutant and AQI patterns.

The model uses the following input features:

| Feature | Description |
|----------|-------------|
| PM25_lag1 | Previous day's PM2.5 |
| PM10_lag1 | Previous day's PM10 |
| NO2_lag1 | Previous day's NO₂ |
| O3_lag1 | Previous day's O₃ |
| SO2_lag1 | Previous day's SO₂ |
| CO_lag1 | Previous day's CO |
| aqi_lag1 | AQI from the previous day |
| aqi_lag3 | AQI from three days earlier |
| aqi_lag7 | AQI from seven days earlier |
| roll_mean_3 | Three-day rolling mean AQI |
| DayOfYear | Day of the year |

These features help the model learn temporal patterns and relationships between historical pollutant concentrations and AQI.

### 3. Machine Learning – Random Forest

A Random Forest Regressor is used to forecast next-day AQI.

The model is trained using historical pollutant and AQI data with engineered lag features.

The trained model and associated model results are saved as serialized `.pkl` files in the `model/` directory and reused by the Streamlit application for predictions and evaluation.

### 4. Explainability – SHAP TreeExplainer

SHAP (SHapley Additive exPlanations) is used to interpret the Random Forest model's predictions.

The project uses **TreeExplainer**, which is designed for tree-based machine learning models.

SHAP values help identify how individual input features contribute to the model's prediction.

The application visualizes feature contributions through a bar chart, helping users understand which historical pollutant and AQI features influenced the predicted value.

### 5. Uncertainty Estimation – Tree-Based Percentiles

Instead of relying only on the average prediction from the Random Forest model, predictions from individual decision trees are collected.

The mean of these tree predictions is used as the predicted AQI, while the 2.5th and 97.5th percentiles are used to estimate the lower and upper prediction values.

This approach provides an indication of prediction variability across the trees in the Random Forest.

**Note:** These estimates represent tree-to-tree prediction spread and should not be interpreted as a calibrated 95% prediction interval or guaranteed range of future AQI values.

## 📈 Model Evaluation

The Random Forest model is evaluated using regression metrics.

| Metric | Result |
|---|---:|
| Mean Absolute Error (MAE) | 19.4780 |
| R² Score | 0.3132 |

The evaluation results are presented through the Streamlit application.

These metrics provide an initial assessment of the model's predictive performance and can serve as a baseline for future improvements.

## 📊 Application Dashboard

The Streamlit application provides different functionalities for exploring air quality data and predictions.

### 1. Pollutant Visualization

Displays historical pollutant concentration trends through line charts.

This allows users to explore changes in pollutant levels over time.

### 2. Next-Day AQI Prediction

Allows users to provide pollutant values and obtain a next-day AQI forecast.

### 3. Uncertainty Estimation

Displays the predicted AQI along with lower and upper estimates derived from the Random Forest tree predictions.

### 4. SHAP Explainability

Visualizes feature contributions through a SHAP-based bar chart to help interpret individual predictions.

### 5. Model Evaluation

Displays model performance metrics, including MAE and R².

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data processing and manipulation |
| NumPy | Numerical computations |
| Scikit-learn | Random Forest model and evaluation |
| SHAP | Model explainability |
| Matplotlib | Data visualization |
| Streamlit | Interactive web application |
| OpenAQ | Pollutant data source |

## 🔮 Future Improvements

- Expand AQI forecasting to multiple districts in Tamil Nadu.
- Integrate additional air quality monitoring stations.
- Experiment with advanced time-series forecasting approaches.
- Improve model performance through feature engineering and hyperparameter tuning.
- Evaluate uncertainty estimates using independent validation data and calibration methods.
- Introduce geographical AQI visualization for district-level comparisons.
- Explore real-time pollutant data integration.

## 🎯 Project Objective

The objective of this project is to build an interactive and interpretable air quality forecasting system that goes beyond conventional point predictions.

By combining machine learning, SHAP-based explainability, and uncertainty estimation, the system aims to provide more transparent and informative AQI forecasts.

### References

**Books**
1. **Molnar, C. (2022).** *Interpretable Machine Learning: A Guide for Making Black Box Models Explainable*. (Excellent resource on SHAP values and model interpretability).
2. **Géron, A. (2019).** *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow*. O'Reilly Media. (Reference for ensemble learning, Random Forests, and hyperparameter tuning).
3. **VanderPlas, J. (2016).** *Python Data Science Handbook: Essential Tools for Working with Data*. O'Reilly Media. (Core text for Pandas functionality, dealing with `.pkl` data and timeseries manipulation).

**Websites & Online Portals**
4. **Scikit-Learn Official Documentation**: [https://scikit-learn.org](https://scikit-learn.org) - Core documentation regarding `RandomForestRegressor` capabilities and tree variance.
5. **SHAP Documentation**: [https://shap.readthedocs.io](https://shap.readthedocs.io) - API guide specifically covering `TreeExplainer` functionalities applied to trees.
6. **Streamlit Framework**: [https://docs.streamlit.io](https://docs.streamlit.io) - Official guides on building interactive Python visualization dashboards.
7. **OpenAQ Platform**: [https://openaq.org](https://openaq.org) - Global, open-source repository for retrieving historical ground-level air quality observations.
8. **Open-Meteo API**: [https://open-meteo.com](https://open-meteo.com) - Open-source weather API utilized for historical climate and wind telemetry.
9. **Central Pollution Control Board (CPCB), India**: [https://cpcb.nic.in](https://cpcb.nic.in) - Official portal publishing national ambient air quality standards and standardized mathematical conversions for the Air Quality Index (AQI).
