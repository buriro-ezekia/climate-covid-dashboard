# Climate and COVID Analytics Dashboard

An interactive analytical dashboard that investigates the relationship between climate conditions and COVID-19 case dynamics using exploratory data analysis, statistical modelling, and time-series forecasting.

The application provides real-time analytical insights through interactive visualisations and predictive modelling.
---

## Project Overview

This project analyses how climate variables such as temperature and humidity relate to COVID-19 case counts. The dashboard allows users to explore patterns, detect anomalies, and generate short-term forecasts of disease trends.

The system integrates statistical analysis, predictive modelling, and interactive visualisation within a single application.

---

## Key Features

• Interactive filters for date range, temperature, and humidity  
• Rolling averages to smooth temporal trends  
• Climate–health regression modelling  
• Time-series forecasting for future COVID-19 cases  
• Seasonality analysis to identify recurring patterns  
• Automated anomaly detection for unusual case spikes  
• Downloadable filtered datasets for further analysis  

---

## Analytical Workflow
\begin{table}[h]
\centering
\caption{Analytical Workflow of the Climate–COVID Dashboard}
\begin{tabular}{ll}
\hline
\textbf{Stage} & \textbf{Description} \\ 
\hline
Data Collection & Gathering climate and COVID-19 case data from structured sources \\

Data Cleaning and Preparation & Handling missing values, formatting dates, and preparing variables for analysis \\

Exploratory Data Analysis & Visualising distributions and relationships between climate variables and case counts \\

Trend Smoothing (Rolling Averages) & Applying rolling statistics to reduce short-term fluctuations in case counts \\

Climate–Case Regression Modelling & Estimating the relationship between climate factors and COVID-19 cases \\

Time-Series Forecasting & Predicting future case trends using historical time-series models \\

Seasonality Decomposition & Identifying recurring temporal patterns in case counts \\

Anomaly Detection & Detecting unusual spikes or drops in case counts using statistical thresholds \\

Interactive Dashboard & Presenting results through an interactive analytical interface \\

\hline
\end{tabular}
\end{table}
---

## Technologies Used

- PostgreSQL
- Python  
- Pandas  
- Plotly  
- Streamlit  
- Scikit-Learn  
- Statsmodels  
---

## Example Insights

The dashboard enables analysis of:

• long-term trends in COVID-19 cases  
• potential associations between climate conditions and infection levels  
• seasonal patterns in disease occurrence  
• anomalous spikes in case counts  
• short-term forecasts of future case trajectories  

---

## Running the Project
git clone https://github.com/buriro-ezekia/climate-covid-dashboard.git

pip install -r requirements.txt

streamlit run app.py


---

## Project Motivation

Understanding environmental influences on infectious diseases is important for public-health preparedness. This project demonstrates how data science techniques can be applied to analyse and visualise climate–health relationships.

---

## Future Improvements

• Integration with real epidemiological datasets  
• Geospatial visualisation of case distribution  
• Advanced forecasting models  
• Automated data pipelines for real-time updates

---
