import mysql.connector

mydb = mysql.connector.connect(
    host='luca.werner.st',
    database='luca_SmartSchool',
    user='luca',
    password='lsgDbpw1!'
)

# create a cursor object to execute SQL queries
mycursor = mydb.cursor()

# define the SQL query to update data
#room = input("Room")
#change = input("Temperature value");

sql = "SELECT Name FROM Buildings"

# execute the SQL query
mycursor.execute(sql)

myresult = mycursor.fetchall()
Buildings = []

for x in myresult:
    Buildings.append(x)


for x in Buildings:
    print(str(x).replace("('", '').replace("',)", ''))

