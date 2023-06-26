import mysql.connector

# connect to the database
mydb = mysql.connector.connect(
    host='luca.werner.st',
    database='luca_SmartSchool',
    user='luca',
    password='lsgDbpw1!'
)

# create a cursor object to execute SQL queries
mycursor = mydb.cursor()

# define the SQL query to update data
sql_select_Buildings = "select Name from Buildings"
mycursor.execute(sql_select_Buildings)
buildings = mycursor.fetchall()
array_buildings = []
for x in buildings:
   array_buildings.append( x[0])
print(array_buildings)
building = input("Building:")

sql_select_Floors = "select FloorName from Floors WHERE Building LIKE '" + building + "'"
mycursor.execute(sql_select_Floors)
floors = mycursor.fetchall()
array_floors = []
for x in floors:
   array_floors.append( x[0][-1])
print(array_floors)
floor = input("Floor:")


sql_select_Rooms = "select Name from Rooms WHERE Floor LIKE '" + building+floor + "'"
mycursor.execute(sql_select_Rooms)
rooms = mycursor.fetchall()
array_rooms = []
for x in rooms:
   array_rooms.append( x[0])
print(array_rooms)
room = input("Room:")
change = input("Temperature value:");

if not building:
    print("Error no Building given")
elif not floor:
    floor = floors
    sql = "UPDATE Heaters JOIN Rooms ON Room = Name JOIN Floors ON Floor = FloorName SET Temperature = '" + change + "' WHERE Building = '" + building + "'"
elif not room:
    room = rooms
    sql = "UPDATE Heaters JOIN Rooms ON Room = Name JOIN Floors ON Floor = FloorName SET Temperature = '" + change + "' WHERE FloorName = '" + building+floor + "'"
else:
    sql = "UPDATE Heaters JOIN Rooms ON Room = Name JOIN Floors ON Floor = FloorName SET Temperature = '" + change +"' WHERE Room = '"+ room +"'"

print(sql)

# execute the SQL query
mycursor.execute(sql)

# commit the changes to the database
mydb.commit()

# print the number of rows affected by the update
print(mycursor.rowcount, "record(s) updated")