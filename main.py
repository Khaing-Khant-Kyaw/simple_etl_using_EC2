from datetime import datetime
from io import StringIO
import os

import boto3
import pandas as pd
import requests
from dotenv import load_dotenv


# Load variables from .env file
load_dotenv()

city_name = "Berlin"
base_url = "https://api.openweathermap.org/data/2.5/weather"

api_key = os.environ.get("OPENWEATHER_API_KEY")
bucket_name = os.environ.get("S3_BUCKET_NAME")

if not api_key:
    raise ValueError("Missing OPENWEATHER_API_KEY environment variable")

if not bucket_name:
    raise ValueError("Missing S3_BUCKET_NAME environment variable")


def kelvin_to_fahrenheit(temp_in_kelvin):
    temp_in_fahrenheit = (temp_in_kelvin - 273.15) * (9 / 5) + 32
    return temp_in_fahrenheit


def upload_to_s3(df, bucket_name, city):
    # Create CSV in memory, not as a local file
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)

    # Create unique S3 file name using timestamp
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    s3_file_name = f"weather_data/{city.lower()}_weather_{timestamp}.csv"

    # Create S3 client using EC2 IAM Role credentials
    s3_client = boto3.client("s3")

    # Upload CSV content directly to S3
    s3_client.put_object(
        Bucket=bucket_name,
        Key=s3_file_name,
        Body=csv_buffer.getvalue(),
        ContentType="text/csv"
    )

    print(f"Uploaded directly to S3: s3://{bucket_name}/{s3_file_name}")


def etl_weather_data():
    params = {
        "q": city_name,
        "appid": api_key
    }

    response = requests.get(base_url, params=params)
    print(response)

    if response.status_code != 200:
        print(response.text)
        raise Exception("API request failed")

    data = response.json()

    city = data["name"]
    weather_description = data["weather"][0]["description"]
    temp_fahrenheit = kelvin_to_fahrenheit(data["main"]["temp"])
    feels_like_fahrenheit = kelvin_to_fahrenheit(data["main"]["feels_like"])
    min_temp_fahrenheit = kelvin_to_fahrenheit(data["main"]["temp_min"])
    max_temp_fahrenheit = kelvin_to_fahrenheit(data["main"]["temp_max"])
    pressure = data["main"]["pressure"]
    humidity = data["main"]["humidity"]
    windspeed = data["wind"]["speed"]

    time_of_record = datetime.utcfromtimestamp(data["dt"] + data["timezone"])
    sunrise_time = datetime.utcfromtimestamp(data["sys"]["sunrise"] + data["timezone"])
    sunset_time = datetime.utcfromtimestamp(data["sys"]["sunset"] + data["timezone"])

    transformed_data = {
        "City": city,
        "Description": weather_description,
        "Temperature(F)": temp_fahrenheit,
        "Feels Like(F)": feels_like_fahrenheit,
        "Minimum Temperature(F)": min_temp_fahrenheit,
        "Maximum Temperature(F)": max_temp_fahrenheit,
        "Pressure": pressure,
        "Humidity": humidity,
        "Wind Speed": windspeed,
        "Time of record": time_of_record,
        "Sunrise (Local Time)": sunrise_time,
        "Sunset (Local Time)": sunset_time
    }

    # Convert one dictionary row into a DataFrame
    df = pd.DataFrame([transformed_data])

    print(df)

    # Upload DataFrame directly to S3
    upload_to_s3(df, bucket_name, city)


etl_weather_data()