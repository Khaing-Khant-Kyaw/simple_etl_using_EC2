OpenWeatherMap ETL Pipeline on AWS EC2
Overview

This project implements a simple ETL (Extract, Transform, Load) pipeline using Python to retrieve real-time weather data from the OpenWeatherMap API. The pipeline extracts current weather information for a specified city, performs basic data transformations, and loads the processed data into a CSV file.

The script is designed to run on an AWS EC2 instance and demonstrates core data engineering concepts such as API ingestion, data transformation, and file-based persistence.

Architecture (Logical Flow)

Extract

Fetches current weather data from the OpenWeatherMap REST API using the requests library.

API authentication is handled using an API key stored externally.

Transform

Converts temperature values from Kelvin to Fahrenheit

Converts Unix timestamps to localized datetime values using timezone offsets

Normalizes nested JSON data into a flat tabular structure

Load

Saves the transformed data into a CSV file using pandas

Technologies Used

Python 3

OpenWeatherMap API

AWS EC2 (Ubuntu)

requests

pandas

datetime

Project Structure
simple_etl_using_EC2/
│
├── main.py
├── README.md
├── requirements.txt
└── .gitignore

Prerequisites

Python 3 installed on the EC2 instance

An active OpenWeatherMap account

Valid OpenWeatherMap API key

Internet access from the EC2 instance

API Key Configuration

The API key is read from an external file to avoid hardcoding secrets.

Create a file named:

credential.txt


Add only your API key inside the file (no quotes, no spaces).

Note: This file must be excluded from Git using .gitignore.

How the Script Works

Defines the target city (London)

Builds the API request URL

Sends an HTTP GET request to OpenWeatherMap

Parses the JSON response

Performs temperature and timestamp conversions

Stores the transformed data in a pandas DataFrame

Writes the output to current_weather_london.csv

How to Run

From the project directory:

python3 main.py


If successful:

The API returns HTTP status 200

A CSV file named current_weather_london.csv is created

Sample Output Columns

City

Description

Temperature (F)

Feels Like (F)

Minimum Temperature (F)

Maximum Temperature (F)

Pressure

Humidity

Wind Speed

Time of Record

Sunrise (Local Time)

Sunset (Local Time)

Limitations

Single city ingestion per execution

File-based storage only (CSV)

API key currently read from text file (can be improved using environment variables)

Future Improvements

Use environment variables for API key management

Parameterize city input

Schedule execution using cron or Airflow

Upload output to Amazon S3

Extend to multi-city ingestion
