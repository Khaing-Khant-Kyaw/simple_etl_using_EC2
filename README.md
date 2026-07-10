# OpenWeatherMap ETL Pipeline on AWS EC2

## Overview

This project implements a simple **ETL (Extract, Transform, Load) pipeline** using **Python** to retrieve real-time weather data from the **OpenWeatherMap API**. The pipeline extracts current weather information for a specified city, performs basic data transformations, and uploads the processed data as a CSV file directly to an **Amazon S3** bucket.

The script is designed to run on an **AWS EC2 (Ubuntu)** instance and demonstrates core data engineering concepts such as API ingestion, data transformation, cloud storage integration, and secure credential handling via environment variables and IAM roles.

---

## Architecture (Logical Flow)

### Extract
- Fetches current weather data from the OpenWeatherMap REST API using the `requests` library
- API authentication is handled via an API key loaded from an environment variable (never hardcoded or committed)

### Transform
- Converts temperature values from **Kelvin to Fahrenheit**
- Converts **Unix timestamps** to localized datetime values using timezone offsets
- Flattens the nested JSON response into a single tabular row using `pandas`

### Load
- Writes the transformed data into an **in-memory CSV buffer** (no local file is created)
- Uploads the CSV directly to an **S3 bucket**, with a timestamped filename (`weather_data/<city>_weather_<timestamp>.csv`) so each run is stored separately
- Uses the EC2 instance's **IAM role** for S3 authentication — no AWS access keys are stored in the code or environment

---

## Technologies Used

- Python 3
- OpenWeatherMap API
- AWS EC2 (Ubuntu)
- AWS S3 (via `boto3`, using EC2 IAM role credentials)
- `requests`
- `pandas`
- `python-dotenv`

---

## Project Structure

```text
simple_etl_using_EC2/
├── .env.example       # Template for required environment variables
├── .gitignore
├── README.md
├── main.py
└── requirements.txt
```

---

## Setup

1. Clone the repo and install dependencies:
```bash
   pip install -r requirements.txt
```
2. Copy `.env.example` to `.env` and fill in your own values:
```bash
   cp .env.example .env
```
3. Make sure the EC2 instance (or your local AWS CLI profile) has permission to `PutObject` on the target S3 bucket.
4. Run the pipeline:
```bash
   python main.py
```

---

## Security Notes

- No credentials are committed to this repository. `OPENWEATHER_API_KEY` and `S3_BUCKET_NAME` are loaded from environment variables via `python-dotenv`.
- AWS access uses the EC2 instance's IAM role rather than static access keys, following AWS's recommended practice for EC2-hosted workloads.
