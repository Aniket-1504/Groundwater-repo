Real-Time Groundwater Resource Evaluation using DWLR Data
A real-time groundwater monitoring and prediction system that ingests live DWLR (Digital Water Level Recorder) sensor data along with weather API feeds to forecast groundwater levels and detect anomalies.
Overview
This project processes 50K+ time-series records to help stakeholders make informed decisions about groundwater resource management. It combines classical ML with deep learning to deliver accurate, seasonally-aware water-level predictions.
Features
Real-time data ingestion from DWLR sensors and weather API feeds
Multi-model ML pipeline:
Random Forest for classification
LSTM networks for time-series forecasting
Trend analysis & anomaly detection on live sensor data
Interactive dashboard with:
Live sensor visualization
Dynamic alerts for abnormal readings
Region-wise groundwater depletion heatmaps
Tech Stack
Layer
Technology
Frontend
React.js
Backend
Node.js
Database
MySQL
ML/Modeling
Python, Scikit-learn, Random Forest, LSTM
External Data
Weather API, DWLR sensor feeds
How It Works
Live DWLR sensor and weather data is ingested and preprocessed.
Data flows through a Random Forest classifier and LSTM forecasting model.
Predictions and anomalies are pushed to a React.js + Node.js dashboard.
Users view live water-level trends, alerts, and depletion heatmaps by region.
Team:

Aniket Kadam
Rutuja Kadam
Sanika Kanchan
Guide: Prof. S. D. Dighe
Institution: Sinhgad Institute of Technology and Science, Pune (SPPU)
Project Status
Completed as a final-year capstone project (2025-26).
