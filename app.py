# -----------------------------------------------------------
# Climate and COVID Dashboard
# -----------------------------------------------------------
# This Streamlit dashboard analyses the relationship between
# climate variables (temperature, humidity) and COVID cases.
#
# The data is loaded from a CSV file stored in the repository,
# making the app compatible with Streamlit Cloud deployment.
# -----------------------------------------------------------


# -----------------------------------------------------------
# IMPORT REQUIRED LIBRARIES
# -----------------------------------------------------------

import streamlit as st
import pandas as pd
import plotly.express as px


# -----------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------

# Configure the dashboard layout and title
st.set_page_config(
    page_title="Climate & COVID Dashboard",
    layout="wide"
)

st.title("Climate and COVID Monitoring Dashboard")


# -----------------------------------------------------------
# LOAD DATASET
# -----------------------------------------------------------

# Cache data for 10 seconds to improve performance
# Streamlit will reload the dataset automatically after cache expires

@st.cache_data(ttl=10)
def load_data():

    # Load dataset from CSV file
    df = pd.read_csv("climate_data.csv")

    # Convert date column to datetime format
    df['date'] = pd.to_datetime(df['date'])

    return df


# Retrieve dataset
df = load_data()


# -----------------------------------------------------------
# KPI METRICS
# -----------------------------------------------------------

# Compute key statistics
total_cases = df['covid_cases'].sum()
avg_temp = round(df['temperature'].mean(), 2)
avg_humidity = round(df['humidity'].mean(), 2)
records = len(df)

# Display KPI cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Cases", total_cases)
col2.metric("Average Temperature", avg_temp)
col3.metric("Average Humidity", avg_humidity)
col4.metric("Number of Records", records)


# -----------------------------------------------------------
# TIME SERIES: COVID CASES
# -----------------------------------------------------------

st.subheader("COVID Cases Over Time")

cases_trend = px.line(
    df,
    x="date",
    y="covid_cases",
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
# SCATTER RELATIONSHIPS
# -----------------------------------------------------------

st.subheader("Climate vs COVID Relationships")

col1, col2 = st.columns(2)

# Temperature vs COVID cases
scatter_temp = px.scatter(
    df,
    x="temperature",
    y="covid_cases",
    title="Temperature vs COVID Cases"
)

# Humidity vs COVID cases
scatter_humidity = px.scatter(
    df,
    x="humidity",
    y="covid_cases",
    title="Humidity vs COVID Cases"
)

col1.plotly_chart(scatter_temp, use_container_width=True)
col2.plotly_chart(scatter_humidity, use_container_width=True)


# -----------------------------------------------------------
# CORRELATION MATRIX
# -----------------------------------------------------------

st.subheader("Correlation Matrix")

# Compute correlations
corr = df[['temperature', 'humidity', 'covid_cases']].corr()

# Plot correlation heatmap
heatmap = px.imshow(
    corr,
    text_auto=True,
    title="Variable Correlation"
)

st.plotly_chart(heatmap, use_container_width=True)


# -----------------------------------------------------------
# DISTRIBUTION CHARTS
# -----------------------------------------------------------

st.subheader("Variable Distributions")

col1, col2, col3 = st.columns(3)

# Temperature distribution
temp_hist = px.histogram(
    df,
    x="temperature",
    title="Temperature Distribution"
)

# Humidity distribution
humidity_hist = px.histogram(
    df,
    x="humidity",
    title="Humidity Distribution"
)

# COVID cases distribution
cases_hist = px.histogram(
    df,
    x="covid_cases",
    title="COVID Cases Distribution"
)

col1.plotly_chart(temp_hist, use_container_width=True)
col2.plotly_chart(humidity_hist, use_container_width=True)
col3.plotly_chart(cases_hist, use_container_width=True)


# -----------------------------------------------------------
# OPTIONAL DATA VIEW
# -----------------------------------------------------------

st.subheader("Dataset Preview")

st.dataframe(df)


# -----------------------------------------------------------
# END OF DASHBOARD
# -----------------------------------------------------------
