# AST_rule_engine
# Real-Time Weather Monitoring and Alerting System
 This application fetches real-time weather data for selected cities, processes and stores daily summaries, and sends alerts if the temperature exceeds a user-defined threshold. The application 
 uses the OpenWeatherMap API for weather data, SQLite for data storage, and matplotlib for data visualization. Alerts are sent via email after consecutive updates indicating temperatures above 
 the threshold.

# Table of Contents
Features
Dependencies
Setup
Usage
Design Choices
Configuration
Database
Troubleshooting
Features
**Real-Time Weather Monitoring: Retrieves weather data for multiple cities at user-defined intervals.**
**Daily Summaries: Stores daily weather summaries (average, max, min temperature) in an SQLite database.**
**Temperature Alerts: Sends an email alert if a city’s temperature exceeds a specified threshold for consecutive updates.**
**Visualization: Plots daily temperature summaries for historical data visualization.**

#Dependencies
This application uses the following dependencies:

Python 3.7+
requests: for API requests.
schedule: for scheduling tasks.
sqlite3: for storing daily weather summaries.
matplotlib: for plotting temperature trends.
smtplib: for sending email alerts.
Install Dependencies
Install required packages using pip:

bash
Copy code
pip install requests schedule matplotlib
Environment Configuration
For this application, you need the following:

API Key: Sign up at OpenWeatherMap to get an API key.
Email Credentials: Configure email credentials for sending alerts.
