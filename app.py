# -----------------------------------------------------------
# Climate and COVID Dashboard
# -----------------------------------------------------------
# Streamlit dashboard analysing the relationship between
# climate variables (temperature, humidity) and COVID cases.
#
# Data is loaded from a CSV file stored in the repository,
# making the app compatible with Streamlit Cloud deployment.
# -----------------------------------------------------------


# -----------------------------------------------------------
# IMPORT REQUIRED LIBRARIES
# -----------------------------------------------------------

import streamlit as st
import pandas as pd
import plotly.express as px
import os


# -----------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------

st.set_page_config(
    page_title="Climate & COVID Dashboard",
    layout="wide"
)

st.title("Climate and COVID Monitoring Dashboard")


# -----------------------------------------------------------
# LOAD DATASET
# -----------------------------------------------------------
@st.cache_data(ttl=10)
def load_data():

    # Load dataset
    df = pd.read_csv("climate_data.csv")

    # Standardise column names (lowercase and remove spaces)
    df.columns = df.columns.str.lower().str.strip()

    # Ensure required column exists
    if "date" not in df.columns:
        st.error("The dataset must contain a 'date' column.")
        st.stop()

    # Convert date column to datetime
    df["date"] = pd.to_datetime(df["date"])

    return df
df = load_data()


# -----------------------------------------------------------
# SIDEBAR FILTERS
# -----------------------------------------------------------

st.sidebar.header("Filter Data")

# Date range filter
start_date = st.sidebar.date_input(
    "Start Date",
    df["date"].min()
)

end_date = st.sidebar.date_input(
    "End Date",
    df["date"].max()
)

# Apply filtering
df = df[(df["date"] >= pd.to_datetime(start_date)) &
        (df["date"] <= pd.to_datetime(end_date))]


# -----------------------------------------------------------
# KPI METRICS
# -----------------------------------------------------------

total_cases = df["covid_cases"].sum()
avg_temp = round(df["temperature"].mean(), 2)
avg_humidity = round(df["humidity"].mean(), 2)
records = len(df)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Cases", total_cases)
col2.metric("Average Temperature", avg_temp)
col3.metric("Average Humidity", avg_humidity)
col4.metric("Number of Records", records)


# -----------------------------------------------------------
# COVID CASES TIME SERIES
# -----------------------------------------------------------

st.subheader("COVID Cases Over Time")

cases_trend = px.line(
    df,
    x="date",
    y="covid_cases",
    markers=True,
    title="COVID Cases Trend"
)

st.plotly_chart(cases_trend, use_container_width=True)


# -----------------------------------------------------------
# CLIMATE TRENDS
# -----------------------------------------------------------

st.subheader("Temperature and Humidity Trends")

climate_trend = px.line(
    df,
    x="date",
    y=["temperature", "humidity"],
    title="Climate Trends"
)

st.plotly_chart(climate_trend, use_container_width=True)


# -----------------------------------------------------------
# CLIMATE vs COVID RELATIONSHIPS
# -----------------------------------------------------------

st.subheader("Climate vs COVID Relationships")

col1, col2 = st.columns(2)

scatter_temp = px.scatter(
    df,
    x="temperature",
    y="covid_cases",
    trendline="ols",
    title="Temperature vs COVID Cases"
)

scatter_humidity = px.scatter(
    df,
    x="humidity",
    y="covid_cases",
    trendline="ols",
    title="Humidity vs COVID Cases"
)

col1.plotly_chart(scatter_temp, use_container_width=True)
col2.plotly_chart(scatter_humidity, use_container_width=True)


# -----------------------------------------------------------
# CORRELATION MATRIX
# -----------------------------------------------------------

st.subheader("Correlation Matrix")

corr = df[["temperature", "humidity", "covid_cases"]].corr()

heatmap = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale="RdBu_r",
    title="Variable Correlation"
)

st.plotly_chart(heatmap, use_container_width=True)


# -----------------------------------------------------------
# DISTRIBUTION CHARTS
# -----------------------------------------------------------

st.subheader("Variable Distributions")

col1, col2, col3 = st.columns(3)

temp_hist = px.histogram(df, x="temperature", nbins=20)
humidity_hist = px.histogram(df, x="humidity", nbins=20)
cases_hist = px.histogram(df, x="covid_cases", nbins=20)

col1.plotly_chart(temp_hist, use_container_width=True)
col2.plotly_chart(humidity_hist, use_container_width=True)
col3.plotly_chart(cases_hist, use_container_width=True)


# -----------------------------------------------------------
# DATA PREVIEW
# -----------------------------------------------------------

st.subheader("Dataset Preview")

st.dataframe(df)


# -----------------------------------------------------------
# FOOTER
# -----------------------------------------------------------

st.caption("Interactive dashboard analysing climate conditions and COVID cases.")
