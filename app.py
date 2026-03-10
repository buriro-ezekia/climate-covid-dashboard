# -----------------------------------------------------------
# Climate and COVID Dashboard (Streamlit Version)
# -----------------------------------------------------------
# This dashboard retrieves data from PostgreSQL and displays
# interactive charts using Streamlit and Plotly.
# -----------------------------------------------------------

# Import required libraries
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# -----------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------

# Configure Streamlit page layout
st.set_page_config(page_title="Climate & COVID Dashboard",
                   layout="wide")

# Dashboard title
st.title("Climate and COVID Monitoring Dashboard")

# -----------------------------------------------------------
# DATABASE CONNECTION
# -----------------------------------------------------------

# Create PostgreSQL connection
engine = create_engine(
    "postgresql://postgres:Chimodoi1810@localhost:5433/data_science_db"
)

# -----------------------------------------------------------
# LOAD DATA FROM DATABASE
# -----------------------------------------------------------

# Function to retrieve data from PostgreSQL
@st.cache_data(ttl=10)
def load_data():

    query = """
        SELECT *
        FROM climate_data
        ORDER BY date
    """

    df = pd.read_sql(query, engine)

    df['date'] = pd.to_datetime(df['date'])

    return df


# Load dataset
df = load_data()

# -----------------------------------------------------------
# KPI CARDS
# -----------------------------------------------------------

# Calculate KPI metrics
total_cases = df['covid_cases'].sum()
avg_temp = round(df['temperature'].mean(),2)
avg_humidity = round(df['humidity'].mean(),2)
records = len(df)

# Display KPI metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Cases", total_cases)
col2.metric("Average Temperature", avg_temp)
col3.metric("Average Humidity", avg_humidity)
col4.metric("Observations", records)

# -----------------------------------------------------------
# TIME SERIES: COVID CASES
# -----------------------------------------------------------

st.subheader("COVID Cases Over Time")

cases_trend = px.line(
    df,
    x='date',
    y='covid_cases'
)

st.plotly_chart(cases_trend, use_container_width=True)

# -----------------------------------------------------------
# CLIMATE TRENDS
# -----------------------------------------------------------

st.subheader("Temperature and Humidity Trends")

climate_trend = px.line(
    df,
    x='date',
    y=['temperature','humidity']
)

st.plotly_chart(climate_trend, use_container_width=True)

# -----------------------------------------------------------
# SCATTER RELATIONSHIPS
# -----------------------------------------------------------

st.subheader("Climate vs COVID Relationships")

col1, col2 = st.columns(2)

scatter_temp = px.scatter(
    df,
    x='temperature',
    y='covid_cases'
)

scatter_humidity = px.scatter(
    df,
    x='humidity',
    y='covid_cases'
)

col1.plotly_chart(scatter_temp, use_container_width=True)
col2.plotly_chart(scatter_humidity, use_container_width=True)

# -----------------------------------------------------------
# CORRELATION HEATMAP
# -----------------------------------------------------------

st.subheader("Correlation Matrix")

corr = df[['temperature','humidity','covid_cases']].corr()

heatmap = px.imshow(corr, text_auto=True)

st.plotly_chart(heatmap, use_container_width=True)

# -----------------------------------------------------------
# DISTRIBUTION CHARTS
# -----------------------------------------------------------

st.subheader("Variable Distributions")

col1, col2, col3 = st.columns(3)

temp_hist = px.histogram(df, x="temperature")
humidity_hist = px.histogram(df, x="humidity")
cases_hist = px.histogram(df, x="covid_cases")

col1.plotly_chart(temp_hist, use_container_width=True)
col2.plotly_chart(humidity_hist, use_container_width=True)
col3.plotly_chart(cases_hist, use_container_width=True)
