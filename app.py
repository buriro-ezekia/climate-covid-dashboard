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
# DATA TABLE
# -----------------------------------------------------------

st.subheader("Filtered Dataset")

st.dataframe(df_filtered)
