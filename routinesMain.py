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
#room = input("Room")
#change = input("Temperature value");

sql = "SELECT * FROM Routines"

# execute the SQL query
cursor.execute(sql)

result = cursor.fetchall()
Routines = []

for x in result:
    Routines.append(x)

print(Routines)

list_routines_hours = list(Routines[4][2])
list_routines_weekdays = list(Routines[4][3])
list_routines_months = list(Routines[4][4])

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

weekday_numbers = [weekday_dict[weekday] for weekday in list_routines_weekdays]
month_numbers = [month_dict[month] for month in list_routines_months]


if str(datetime.now().hour) in list_routines_hours \
        and datetime.now().weekday() in weekday_numbers \
        and datetime.now().month in month_numbers:
    print("true")
else:
    print("False")
