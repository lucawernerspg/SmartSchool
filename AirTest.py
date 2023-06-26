import mysql.connector
from datetime import date, datetime, timedelta
import numpy as np
from sklearn.linear_model import LinearRegression

today = date.today()
timetosubtract = input("Days to subtract")
timeframe = today-timedelta(days=int(timetosubtract))
print(timeframe)

def learn_correlation(data):
    # Extract the feature and target values from the data
    X = np.array([x[0] for x in data]).reshape(-1, 1)  # Feature (independent variable)
    y = np.array([x[1] for x in data])                # Target (dependent variable)

    # Create a Linear Regression model
    model = LinearRegression()

    # Fit the model to the data
    model.fit(X, y)

    # Retrieve the coefficients (slope and intercept)
    slope = model.coef_[0]
    intercept = model.intercept_

    return slope, intercept




connection = mysql.connector.connect(
        host='luca.werner.st',
        user='luca',
        password='lsgDbpw1!',
        database='luca_SmartSchool'
    )
cursor = connection.cursor()



sql_select_Weather = "select Date, Temperature, Humidity from Weather WHERE Date >" + str(timeframe)
sql_select_RoomAir = "select Date, Temperature, Humidity from RoomAir WHERE Date >" + str(timeframe)

cursor.execute(sql_select_Weather)
weather = cursor.fetchall()

cursor.execute(sql_select_RoomAir)
roomair = cursor.fetchall()




array_roomair = []
array_weather = []
for row in roomair:
    array_roomair.append(row)

for row in weather:
    array_weather.append(row)

min_table_size = min(len(array_weather),len(array_roomair))

print(min_table_size)

#for x in array_roomair:
    #print("roomair")
    #print(x[0])

#for row in array_weather:
    #print("weather")
    #print(row[0])

array_matching_dates = []
for x in range(min_table_size):
    if array_weather[x][0].year == array_roomair[x][0].year \
            and array_weather[x][0].month == array_roomair[x][0].month :
            #and array_weather[x][0].day == array_roomair[x][0].day\
            #and array_weather[x][0].hour == array_roomair[x][0].hour:
        #print(array_weather[x][0].year , array_weather[x][0].month, array_weather[x][0].day, array_weather[x][0].hour)
        array_matching_dates.append(x)

    #else:
        #print("false")

array_temperatures = []

for x in array_matching_dates:
    array_temperatures.append(tuple([array_weather[x][1],array_roomair[x][1]]))

array_humidity = []

for x in array_matching_dates:
    array_humidity.append(tuple([array_weather[x][2],array_roomair[x][2]]))

#print(array_temperatures)
#for x in array_temperatures:
    #print(x)

slope, intercept = learn_correlation(array_temperatures)
print("Temperature Slope:", slope)
print("Temperature Intercept:", intercept)

slope, intercept = learn_correlation(array_humidity)
print("Humidity Slope:", slope)
print("Humidity Intercept:", intercept)