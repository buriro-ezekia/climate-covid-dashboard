# -----------------------------------------------------------
# Climate and COVID Analytical Dashboard
# -----------------------------------------------------------
# Advanced dashboard including:
# - interactive filters
# - rolling averages
# - predictive modelling
# - seasonality analysis
# -----------------------------------------------------------

import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np


# -----------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------

st.set_page_config(page_title="Climate & COVID Dashboard", layout="wide")

st.title("Climate and COVID Monitoring Dashboard")


# -----------------------------------------------------------
# LOAD DATA
# -----------------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv("climate_data.csv")

    df.columns = df.columns.str.lower().str.strip()

    df["date"] = pd.to_datetime(df["date"])

    return df


df = load_data()


# -----------------------------------------------------------
# INTERACTIVE FILTERS
# -----------------------------------------------------------

st.sidebar.header("Data Filters")

date_range = st.sidebar.date_input(
    "Select Date Range",
    [df["date"].min(), df["date"].max()]
)

temp_range = st.sidebar.slider(
    "Temperature Range",
    float(df["temperature"].min()),
    float(df["temperature"].max()),
    (float(df["temperature"].min()), float(df["temperature"].max()))
)

humidity_range = st.sidebar.slider(
    "Humidity Range",
    float(df["humidity"].min()),
    float(df["humidity"].max()),
    (float(df["humidity"].min()), float(df["humidity"].max()))
)

df_filtered = df[
    (df["date"] >= pd.to_datetime(date_range[0])) &
    (df["date"] <= pd.to_datetime(date_range[1])) &
    (df["temperature"].between(temp_range[0], temp_range[1])) &
    (df["humidity"].between(humidity_range[0], humidity_range[1]))
]


# -----------------------------------------------------------
# KPI METRICS
# -----------------------------------------------------------

st.subheader("Key Indicators")

col1, col2, col3 = st.columns(3)

col1.metric("Total Cases", int(df_filtered["covid_cases"].sum()))
col2.metric("Average Temperature", round(df_filtered["temperature"].mean(), 2))
col3.metric("Average Humidity", round(df_filtered["humidity"].mean(), 2))


# -----------------------------------------------------------
# ROLLING AVERAGE TREND
# -----------------------------------------------------------

st.subheader("COVID Cases Trend with Rolling Average")

df_filtered["rolling_cases"] = df_filtered["covid_cases"].rolling(window=7).mean()

trend_fig = px.line(
    df_filtered,
    x="date",
    y=["covid_cases", "rolling_cases"],
    title="Daily Cases and 7-Day Rolling Average"
)

st.plotly_chart(trend_fig, use_container_width=True)


# -----------------------------------------------------------
# CLIMATE RELATIONSHIPS
# -----------------------------------------------------------

st.subheader("Climate Relationships")

col1, col2 = st.columns(2)

temp_scatter = px.scatter(
    df_filtered,
    x="temperature",
    y="covid_cases",
    trendline="ols",
    title="Temperature vs COVID Cases"
)

humidity_scatter = px.scatter(
    df_filtered,
    x="humidity",
    y="covid_cases",
    trendline="ols",
    title="Humidity vs COVID Cases"
)

col1.plotly_chart(temp_scatter, use_container_width=True)
col2.plotly_chart(humidity_scatter, use_container_width=True)


# -----------------------------------------------------------
# SEASONALITY ANALYSIS
# -----------------------------------------------------------

st.subheader("Monthly Seasonality")

df_filtered["month"] = df_filtered["date"].dt.month

monthly_cases = df_filtered.groupby("month")["covid_cases"].mean().reset_index()

season_fig = px.bar(
    monthly_cases,
    x="month",
    y="covid_cases",
    title="Average Monthly COVID Cases"
)

st.plotly_chart(season_fig, use_container_width=True)


# -----------------------------------------------------------
# PREDICTIVE MODEL
# -----------------------------------------------------------

st.subheader("Predictive Model: Climate → COVID Cases")

X = df_filtered[["temperature", "humidity"]]
y = df_filtered["covid_cases"]

model = LinearRegression()

model.fit(X, y)

temp_input = st.slider("Temperature for prediction", 15.0, 40.0, 25.0)
humidity_input = st.slider("Humidity for prediction", 20.0, 90.0, 60.0)

prediction = model.predict([[temp_input, humidity_input]])

st.write(
    f"Predicted COVID cases for temperature {temp_input}°C "
    f"and humidity {humidity_input}%: **{int(prediction[0])} cases**"
)

# -----------------------------------------------------------
# TIME-SERIES FORECASTING (30-DAY PREDICTION)
# -----------------------------------------------------------

import statsmodels.api as sm

st.subheader("30-Day COVID Case Forecast")

# Prepare time-series data
ts = df_filtered.set_index("date")["covid_cases"]

# Fit ARIMA model
model = sm.tsa.ARIMA(ts, order=(2,1,2))
results = model.fit()

# Forecast next 30 days
forecast_steps = 30
forecast = results.forecast(steps=forecast_steps)

# Create future dates
future_dates = pd.date_range(
    start=ts.index.max() + pd.Timedelta(days=1),
    periods=forecast_steps
)

forecast_df = pd.DataFrame({
    "date": future_dates,
    "forecast_cases": forecast
})

# Combine historical and forecast data
historical_df = ts.reset_index()
historical_df.columns = ["date","cases"]

forecast_df_plot = forecast_df.rename(columns={"forecast_cases":"cases"})

combined = pd.concat([historical_df, forecast_df_plot])

# Plot forecast
forecast_fig = px.line(
    combined,
    x="date",
    y="cases",
    title="Historical and Forecasted COVID Cases"
)

st.plotly_chart(forecast_fig, use_container_width=True)

# -----------------------------------------------------------
# TIME-SERIES DECOMPOSITION (TREND + SEASONALITY)
# -----------------------------------------------------------

import statsmodels.api as sm

st.subheader("Trend and Seasonality Analysis")

# Prepare time-series data
ts = df_filtered.set_index("date")["covid_cases"]

# Ensure regular frequency
ts = ts.asfreq("D")

# Fill missing values if necessary
ts = ts.fillna(method="ffill")

# Decompose the time series
decomposition = sm.tsa.seasonal_decompose(ts, model="additive", period=30)

trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

# Convert components to DataFrame
decomp_df = pd.DataFrame({
    "date": ts.index,
    "trend": trend,
    "seasonal": seasonal,
    "residual": residual
})

# Plot trend
trend_fig = px.line(
    decomp_df,
    x="date",
    y="trend",
    title="Long-Term Trend in COVID Cases"
)

st.plotly_chart(trend_fig, use_container_width=True)

# Plot seasonal pattern
seasonal_fig = px.line(
    decomp_df,
    x="date",
    y="seasonal",
    title="Seasonal Pattern"
)

st.plotly_chart(seasonal_fig, use_container_width=True)

# -----------------------------------------------------------
# ANOMALY DETECTION
# -----------------------------------------------------------

st.subheader("Anomaly Detection")

# Detect anomalies using standard deviation threshold
mean_cases = ts.mean()
std_cases = ts.std()

threshold_upper = mean_cases + 2 * std_cases
threshold_lower = mean_cases - 2 * std_cases

anomalies = ts[(ts > threshold_upper) | (ts < threshold_lower)]

anomaly_df = ts.reset_index()
anomaly_df.columns = ["date","cases"]

anomaly_fig = px.scatter(
    anomaly_df,
    x="date",
    y="cases",
    title="Detected Anomalies in COVID Cases"
)

# Highlight anomaly points
anomaly_fig.add_scatter(
    x=anomalies.index,
    y=anomalies.values,
    mode="markers",
    marker=dict(color="red", size=8),
    name="Anomaly"
)

st.plotly_chart(anomaly_fig, use_container_width=True)


# -----------------------------------------------------------
# DATA TABLE
# -----------------------------------------------------------

st.subheader("Filtered Dataset")

st.dataframe(df_filtered)
