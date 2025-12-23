# OpenWeatherMap ETL Pipeline on AWS EC2

## Overview

This project implements a simple **ETL (Extract, Transform, Load) pipeline** using **Python** to retrieve real-time weather data from the **OpenWeatherMap API**. The pipeline extracts current weather information for a specified city, performs basic data transformations, and loads the processed data into a CSV file.

The script is designed to run on an **AWS EC2 (Ubuntu)** instance and demonstrates core data engineering concepts such as API ingestion, data transformation, and file-based persistence.

---

## Architecture (Logical Flow)

### Extract
- Fetches current weather data from the OpenWeatherMap REST API using the `requests` library
- API authentication is handled using an API key

### Transform
- Converts temperature values from **Kelvin to Fahrenheit**
- Converts **Unix timestamps** to localized datetime values using timezone offsets
- Flattens nested JSON responses into a tabular structure

### Load
- Writes the transformed data into a **CSV file** using `pandas`

---

## Technologies Used

- Python 3
- OpenWeatherMap API
- AWS EC2 (Ubuntu)
- requests
- pandas
- datetime

---

## Project Structure
simple_etl_using_EC2/
├── .gitignore
├── README.md
├── credential.txt
├── main.py
└── requirements.txt

