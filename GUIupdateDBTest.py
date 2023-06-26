import tkinter as tk
import mysql.connector
from tkinter import ttk

# Connect to the database
mydb = mysql.connector.connect(
    host='luca.werner.st',
    database='luca_SmartSchool',
    user='luca',
    password='lsgDbpw1!'
)

# Create the main window
window = tk.Tk()
window.title("Temperature Control")
window.geometry("400x300")

# Create a frame for the picker widgets
picker_frame = tk.Frame(window)
picker_frame.pack(pady=20)

# Create the building picker
building_label = tk.Label(picker_frame, text="Building:")
building_label.grid(row=0, column=0, padx=10)

building_picker = ttk.Combobox(picker_frame, state="readonly")
building_picker.grid(row=0, column=1, padx=10)

# Create the floor picker
floor_label = tk.Label(picker_frame, text="Floor:")
floor_label.grid(row=1, column=0, padx=10)

floor_picker = ttk.Combobox(picker_frame, state="readonly")
floor_picker.grid(row=1, column=1, padx=10)

# Create the room picker
room_label = tk.Label(picker_frame, text="Room:")
room_label.grid(row=2, column=0, padx=10)

room_picker = ttk.Combobox(picker_frame, state="readonly")
room_picker.grid(row=2, column=1, padx=10)

# Create the temperature entry field
change_label = tk.Label(window, text="Temperature value:")
change_label.pack()

change_entry = tk.Entry(window)
change_entry.pack()

# Create a function to populate the picker options
def populate_picker_options(event=None):
    selected_building = building_picker.get()
    selected_floor = floor_picker.get()

    mycursor = mydb.cursor()

    if not selected_building:
        building_picker["values"] = []
        floor_picker["values"] = []
        room_picker["values"] = []
        return

    # Retrieve the floors for the selected building
    sql_select_floors = "SELECT FloorName FROM Floors WHERE Building LIKE %s"
    values = (selected_building,)
    mycursor.execute(sql_select_floors, values)
    floors = mycursor.fetchall()

    # Populate the floor picker
    floor_options = ["All"] + [floor[0][-1] for floor in floors]
    floor_picker["values"] = floor_options

    # Set the selected floor if it exists in the updated options
    if selected_floor in floor_options:
        floor_picker.set(selected_floor)
    else:
        floor_picker.current(0)

    if not selected_floor:
        room_picker["values"] = []
        return

    # Retrieve the rooms for the selected building and floor
    sql_select_rooms = "SELECT Name FROM Rooms WHERE Floor LIKE %s"
    if selected_floor == "All":
        values = (selected_building + "%",)
    else:
        values = (selected_building + selected_floor,)

    mycursor.execute(sql_select_rooms, values)
    rooms = mycursor.fetchall()

    # Populate the room picker
    room_options = ["All"] + [room[0] for room in rooms]
    room_picker["values"] = room_options
    room_picker.current(0)

# Create a function to update the temperature
def update_temperature():
    building = building_picker.get()
    floor = floor_picker.get()
    room = room_picker.get()
    change = change_entry.get()

    sql = "UPDATE Heaters JOIN Rooms ON Room = Name JOIN Floors ON Floor = FloorName SET Temperature = %s"

    values = (change,)

    if building and building != "All":
        sql += " WHERE Building = %s"
        values += (building,)

        if floor and floor != "All":
            sql += " AND FloorName = %s"
            values += (building + floor,)

            if room and room != "All":
                sql += " AND Room = %s"
                values += (room,)

    mycursor = mydb.cursor()
    mycursor.execute(sql, values)
    mydb.commit()

    result_label.config(text=str(mycursor.rowcount) + " record(s) updated")

# Create a button to update the temperature
update_button = tk.Button(window, text="Update", command=update_temperature)
update_button.pack()

# Create a label to display the result
result_label = tk.Label(window, text="")
result_label.pack()

# Populate the building picker
mycursor = mydb.cursor()
sql_select_buildings = "SELECT Name FROM Buildings"
mycursor.execute(sql_select_buildings)
buildings = mycursor.fetchall()

building_options = ["All"] + [building[0] for building in buildings]
building_picker["values"] = building_options
building_picker.bind("<<ComboboxSelected>>", populate_picker_options)

# Configure event bindings for picker options
building_picker.bind("<<ComboboxSelected>>", populate_picker_options)
floor_picker.bind("<<ComboboxSelected>>", populate_picker_options)

# Run the GUI event loop
window.mainloop()