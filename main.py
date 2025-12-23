import json
from datetime import datetime
import pandas as pandas
import requests

city_name = 'London'
base_url =  'https://api.openweathermap.org/data/2.5/weather?q='

with open('credential.txt','r') as f:
    api_key = f.read()

full_url = base_url+ city_name+ '&appid='+api_key

def kelvin_to_fahrenheit(temp_in_kelvin):
    temp_in_fahrenheit = (temp_in_kelvin - 273.15)*(9/5)+32
    return temp_in_fahrenheit

def etl_weahter_data(url):
    r = requests.get(url)
    print(r)
    data = r.json()
    #print(data)

    city = data['name']
    weather_description = data['weather'][0]['description']
    temp_fahrenheit = kelvin_to_fahrenheit(data['main']['temp'])
    feels_like_fahrenheit = kelvin_to_fahrenheit(data['main']['feels_like'])
    min_temp_fahrenheit = kelvin_to_fahrenheit(data['main']['temp_min'])
    max_temp_fahrenheit = kelvin_to_fahrenheit(data['main']['temp_max'])
    pressure = data['main']['pressure']
    humidity = data['main']['humidity']
    windspeed = data['wind']['speed']
    time_of_record = datetime.utcfromtimestamp(data['dt']+data['timezone'])
    sunrise_time = datetime.utcfromtimestamp(data['sys']['sunrise']+data['timezone'])
    sunset_time = datetime.utcfromtimestamp(data['sys']['sunset']+data['timezone'])

    transformed_data = {'City': city,
                        'Description':weather_description,
                        'Temperature(F)': temp_fahrenheit,
                        'Feels Like(F)': feels_like_fahrenheit,
                        'Minimum Temperature(F)': min_temp_fahrenheit,
                        'Maximum Temperature(F)':max_temp_fahrenheit,
                        'Pressure': pressure,
                        'Humidity':humidity,
                        'Wind Speed':windspeed,
                        'Time of record': time_of_record,
                        'Sunrise (Local Time)': sunrise_time,
                        'Sunset (Local Time)': sunset_time}

    #print(transformed_data)
    transformed_data_list = [transformed_data] 
    #print(transformed_data_list)
    df = pandas.DataFrame(transformed_data_list)
    print(df)
    df.to_csv('current_weather_london.csv', index = False)


etl_weahter_data(full_url)