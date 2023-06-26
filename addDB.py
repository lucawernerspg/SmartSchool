import mysql.connector

def add_entry_to_db(connection, name, heaters, windows, capacity):
    try:
        cursor = connection.cursor()
        sql_query = "INSERT INTO Rooms (Name, Heaters, Windows, Capacity) VALUES (%s, %s, %s, %s)"
        data = (name, heaters, windows, capacity)
        cursor.execute(sql_query, data)
        connection.commit()
        print(cursor.rowcount, "record inserted.")
    except mysql.connector.Error as e:
        print("Error inserting data into MySQL table", e)

# example usage
connection = mysql.connector.connect(host='luca.werner.st',
                                                 database='luca_SmartSchool',
                                                 user='luca',
                                                 password='lsgDbpw1!')

roomname = input("Enter Roomname: ")
heaterstemp = input("Enter Heater Temperature: ")
windowscount = input("Enter Number of Windows: ")
capacitynumber = input("Enter the number of people that can be in this room:")

add_entry_to_db(connection, roomname, heaterstemp, windowscount, capacitynumber)

connection.close()

#INSERT INTO `Routines` (`ID`, `Name`, `HoursActive`, `DaysActive`, `MonthsActive`) VALUES ('1', 'Test', '8,9,10,11,12,13,14,15,16', 'Monday,Tuesday,Wednesday,Thursday,Friday', 'January,February,March,April,May,June,September,October,November,December');