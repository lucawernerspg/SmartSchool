from statistics import mean
import datetime
import mysql.connector
from datetime import date, datetime, timedelta

today = date.today()
timetosubtract = input("Days to subtract")
timeframe = today-timedelta(days=int(timetosubtract))
print(timeframe)

mydb = mysql.connector.connect(
    host='luca.werner.st',
    database='luca_SmartSchool',
    user='luca',
    password='lsgDbpw1!'
)

mycursor = mydb.cursor()


sql = ("SELECT AVG(Temperature), AVG(Humidity), AVG(Windspeed) FROM Weather WHERE Date >" + str(timeframe))

mycursor.execute(sql)


myresult = mycursor.fetchone()

print("Temperature: " + str(myresult[0]))
print("Humidity: " + str(myresult[1]))
print("Windspeed: " + str(myresult[2]))



