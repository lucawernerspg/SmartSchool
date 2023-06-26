import requests
import json
import mysql.connector
from datetime import datetime
import threading

def weather():
    threading.Timer(600.0, weather).start()
    api_key = 'f6cd76c92dcf002eeb4f67efaf1c40a3'
    location = 'Vienna'

    # Make request to OpenWeatherMap API
    url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric'
    response = requests.get(url)

    if response.status_code != 200:
        print(f'Unable to get current weather information. Status code: {response.status_code}')
        exit()

    # Parse JSON response
    data = json.loads(response.text)

    # Get current weather
    temperature = data['main']['temp']
    description = data['weather'][0]['description']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']

    print(f'Current temperature in {location}: {temperature}°C')
    print(f'Weather description: {description}')
    print(f'Humidity: {humidity}%')
    print(f'Wind speed: {wind_speed} m/s')

    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    print (dt_string)

    def add_entry_to_db(connection, date, description, temperature, humidity, windspeed):
        try:
            cursor = connection.cursor()
            sql_query = "INSERT INTO Weather (Date, Description, Temperature, Humidity, Windspeed) VALUES (%s, %s, %s, %s, %s)"
            data = (dt_string, description, temperature, humidity, wind_speed)
            cursor.execute(sql_query, data)
            connection.commit()
            print(cursor.rowcount, "record inserted.")
        except mysql.connector.Error as e:
            print("Error inserting data into MySQL table", e)

    connection = mysql.connector.connect(host='luca.werner.st',
                                                     database='luca_SmartSchool',
                                                     user='luca',
                                                     password='lsgDbpw1!')

    add_entry_to_db(connection, dt_string, description, temperature, humidity, wind_speed)

    connection.close()

    # Get weather statistics
    url = f'https://api.openweathermap.org/data/2.5/onecall?lat={data["coord"]["lat"]}&lon={data["coord"]["lon"]}&exclude=current,minutely,hourly&appid={api_key}&units=metric'
    response = requests.get(url)

    if response.status_code != 200:
        print(f'Unable to get weather statistics. Status code: {response.status_code}')
        exit()

    # Parse JSON response
    data = json.loads(response.text)

    # Get weather statistics for each day
    stats = {}
    for item in data['daily']:
        date = item['dt']
        min_temp = item['temp']['min']
        max_temp = item['temp']['max']
        stats[date] = {'min_temp': min_temp, 'max_temp': max_temp}

    # Print weather statistics
    print('\nWeather statistics:')
    for date, values in stats.items():
        print(f'{date}: min {values["min_temp"]}°C, max {values["max_temp"]}°C')

weather()