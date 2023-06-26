import mysql.connector

# Connect to the database
connection = mysql.connector.connect(host='luca.werner.st',
                                                 database='luca_SmartSchool',
                                                 user='luca',
                                                 password='lsgDbpw1!')


# Get a cursor
cursor = connection.cursor()

# Define the SQL statement
sql = "DELETE FROM Rooms WHERE Name = %s"

# Prompt the user for the ID of the row to delete
id_to_delete = input("Enter the Name of the Room to delete: ")

# Execute the SQL statement
cursor.execute(sql, (id_to_delete,))

# Commit the changes to the database
connection.commit()

# Print a message indicating the number of rows deleted
print("{} row(s) deleted.".format(cursor.rowcount))

# Close the cursor and database connection
cursor.close()
connection.close()