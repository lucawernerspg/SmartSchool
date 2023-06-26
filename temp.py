import tkinter
from tkinter import *
from tkinter import ttk, Entry
from tkinter import messagebox
import datetime
import mysql.connector
#print(datetime.date.today().weekday())
#print(datetime.date.today().month)

#-------------------------------Functions-----------------------------------

def Close():
    window.destroy()


def selected_item():
    # Traverse the tuple returned by
    # curselection method and print
    # corresponding value(s) in the listbox
    for i in weekday_list.curselection():
        selected_weekdays.append(weekday_list.get(i))
    for x in months_list.curselection():
        selected_months.append(months_list.get(x))
    for y in hours_list.curselection():
        selected_hours.append(hours_list.get(y))
    global routineName
    routineName = (routine_name_entry.get())
    global temperature
    temperature = temperature_entry.get()

def add_entry_to_db(connection, name, HoursActive, DaysActive, MonthsActive):
    try:
        cursor = connection.cursor()
        sql_query = "INSERT INTO Routines (Name, HoursActive, DaysActive, MonthsActive, Temperature) VALUES (%s, %s, %s, %s, %s)"
        data = (name, HoursActive, DaysActive, MonthsActive, temperature)
        cursor.execute(sql_query, data)
        connection.commit()
        print(cursor.rowcount, "record inserted.")
    except mysql.connector.Error as e:
        print("Error inserting data into MySQL table", e)

#-----------------------------Variables-----------------------
selected_weekdays = []
selected_months = []
selected_hours = []
routineName = ""
temperature = 0
#--------------------------------window----------------------------------------------

window = tkinter.Tk()
window.title("Create Routine Form")

#----------------------------months selection-----------------------------
months_selection_label = Label(window,
              text = "Select the months below :  ",
              padx = 10, pady = 10)
months_selection_label.pack()
months_list = Listbox(window, selectmode = "extended",  exportselection=0)
months_list.pack(padx=10, pady=10,
          expand=YES, fill="both")

x = ["January", "February", "March", "April", "May",
     "June", "July", "August", "September", "October", "November", "December"]

for each_item in range(len(x)):
    months_list.insert(12, x[each_item])
#------------------------------weekdays selection-----------------------------
weekday_selection_label = Label(window,
              text = "Select the weekdays below :  ",
              padx = 10, pady = 10)
weekday_selection_label.pack()
weekday_list = Listbox(window, selectmode = "extended",  exportselection=0)
weekday_list.pack(padx=10, pady=10,
          expand=YES, fill="both")
i = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

for each_item in range(len(i)):
    weekday_list.insert(7, i[each_item])

#------------------------------hours selection--------------------------------
hours_selection_label = Label(window,
              text = "Select the hours below :  ",
              padx = 10, pady = 10)
hours_selection_label.pack()
hours_list = Listbox(window, selectmode = "extended",  exportselection=0)
hours_list.pack(padx=10, pady=10,
          expand=YES, fill="both")
i = ["0", "1", "2", "3", "4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]

for each_item in range(len(i)):
    hours_list.insert(24, i[each_item])

#------------------------------------Form-----------------------------------------------------------
frame = tkinter.Frame(window)
frame.pack()

routine_values_frame = tkinter.LabelFrame(frame, text="Routine values")
routine_values_frame.grid(row=0, column=0, padx=20, pady=10)

routine_name_label = tkinter.Label(routine_values_frame, text="Routine Name")
routine_name_label.grid(row=0, column=0)
routine_name_entry: Entry = tkinter.Entry(routine_values_frame)
routine_name_entry.grid(row=1, column=0)

temperature_label = tkinter.Label(routine_values_frame, text="Temperature")
temperature_label.grid(row=0, column=1)
temperature_entry = tkinter.Spinbox(routine_values_frame, from_=0, to=100)
temperature_entry.grid(row=1, column=1)


button = tkinter.Button(frame, text="Submit", command=lambda: [ selected_item(), Close()])
button.grid(row=3, column=0, sticky="news", padx=20, pady=10)


window.mainloop()
"""""
for i in selected_weekdays:
    print(i)

for x in selected_months:
    print(x)

for x in selected_hours:
    print(x)
"""""
connection = mysql.connector.connect(host='luca.werner.st', database='luca_SmartSchool', user='luca', password='lsgDbpw1!')

test_var = routine_name_entry


HoursActive = ','.join(selected_hours)
DaysActive = ','.join(selected_weekdays)
MonthsActive = ','.join(selected_months)

print(selected_hours)
print(HoursActive)
print(DaysActive)
print(MonthsActive)
print(routineName)
print(temperature)

#add_entry_to_db(connection, routineName, HoursActive, DaysActive, MonthsActive)

connection.close()