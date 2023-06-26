import tkinter as tk
import mysql.connector
from datetime import date, timedelta
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

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

def get_matching_dates():
    today = date.today()
    timetosubtract = int(entry.get())
    timeframe = today - timedelta(days=timetosubtract)
    print(timeframe)

    connection = mysql.connector.connect(
        host='luca.werner.st',
        user='luca',
        password='lsgDbpw1!',
        database='luca_SmartSchool'
    )
    cursor = connection.cursor()

    sql_select_Weather = "select Date, Temperature, Humidity from Weather WHERE Date > %s"
    sql_select_RoomAir = "select Date, Temperature, Humidity from RoomAir WHERE Date > %s"

    cursor.execute(sql_select_Weather, (timeframe,))
    weather = cursor.fetchall()

    cursor.execute(sql_select_RoomAir, (timeframe,))
    roomair = cursor.fetchall()

    array_roomair = [row for row in roomair]
    array_weather = [row for row in weather]

    min_table_size = min(len(array_weather), len(array_roomair))

    array_matching_dates = []
    for x in range(min_table_size):
        if array_weather[x][0].year == array_roomair[x][0].year and \
                array_weather[x][0].month == array_roomair[x][0].month:
            array_matching_dates.append(x)

    array_temperatures = [(array_weather[x][1], array_roomair[x][1]) for x in array_matching_dates]
    array_humidity = [(array_weather[x][2], array_roomair[x][2]) for x in array_matching_dates]

    slope_temp, intercept_temp = learn_correlation(array_temperatures)
    slope_humidity, intercept_humidity = learn_correlation(array_humidity)

    result_label.config(text=f"Temperature Slope: {slope_temp}\n"
                             f"Temperature Intercept: {intercept_temp}\n"
                             f"Humidity Slope: {slope_humidity}\n"
                             f"Humidity Intercept: {intercept_humidity}")

    # Plotting the regression lines
    X_temp = np.array([x[0] for x in array_temperatures])
    y_temp = np.array([x[1] for x in array_temperatures])
    X_humidity = np.array([x[0] for x in array_humidity])
    y_humidity = np.array([x[1] for x in array_humidity])

    plt.figure(figsize=(8, 6))
    plt.scatter(X_temp, y_temp, color='blue', label='Temperature')
    plt.scatter(X_humidity, y_humidity, color='red', label='Humidity')

    plt.plot(X_temp, slope_temp * X_temp + intercept_temp, color='blue')
    plt.plot(X_humidity, slope_humidity * X_humidity + intercept_humidity, color='red')

    plt.xlabel('Weather')
    plt.ylabel('Room Air')
    plt.title('Correlation between Weather and Room Air')
    plt.legend()
    plt.show()

# Create the GUI window
window = tk.Tk()
window.title("Linear Regression Analysis")
window.geometry("300x200")

# Create input field and label
label = tk.Label(window, text="Days to subtract:")
label.pack()

entry = tk.Entry(window)
entry.pack()

# Create button
button = tk.Button(window, text="Get Correlation", command=get_matching_dates)
button.pack()

# Create output label
result_label = tk.Label(window, text="")
result_label.pack()

# Run the GUI event loop
window.mainloop()