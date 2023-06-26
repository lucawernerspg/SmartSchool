from array import array
from enum import Enum
import schedule
import time
from datetime import date, datetime, timedelta
import mysql.connector
import locale

# Connect to the database
conn = mysql.connector.connect(
    host='luca.werner.st',
    database='luca_SmartSchool',
    user='luca',
    password='lsgDbpw1!'
)

cursor = conn.cursor()

# define the SQL query to update data

sql = "SELECT * FROM Routines"

# execute the SQL query
cursor.execute(sql)

result = cursor.fetchall()
Routines = []

for x in result:
    Routines.append(x)



current_datetime = datetime.now()
current_hour = current_datetime.hour
current_weekday = current_datetime.weekday()  # Monday is 0 and Sunday is 6
current_month = current_datetime.month

weekday_dict = {
    'Monday': 0,
    'Tuesday': 1,
    'Wednesday': 2,
    'Thursday': 3,
    'Friday': 4,
    'Saturday': 5,
    'Sunday': 6
}

month_dict = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12
}

for routine in Routines:
    routine_name = routine[1]
    routine_hours = routine[2]
    routine_weekdays = routine[3]
    routine_months = routine[4]
    routine_temperature = routine[5]

    weekday_numbers = [weekday_dict[weekday] for weekday in routine_weekdays]
    month_numbers = [month_dict[month] for month in routine_months]

    if str(current_hour) in routine_hours and current_weekday in weekday_numbers and current_month in month_numbers:
        print(f"{routine_name}: True")
        print(routine_temperature)
    else:
        print(f"{routine_name}: False")