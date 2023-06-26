import tkinter as tk
import mysql.connector
from tkinter import messagebox

class DataEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Data Editor")
        self.geometry("1800x600")
        self.create_table()


    def create_table(self):
        # Connect to the database
        db = mysql.connector.connect(
            host='luca.werner.st',
            database='luca_SmartSchool',
            user='luca',
            password='lsgDbpw1!'
        )

        # Retrieve data from the table
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Routines")
        rows = cursor.fetchall()

        # Create a table to display the data
        table = tk.Frame(self)
        table.pack(fill=tk.BOTH, expand=True)

        # Create table headers
        headers = ["ID", "Name", "Hours", "Weekdays", "Months", "Temperature", "Actions"]
        for col, header in enumerate(headers):
            label = tk.Label(table, text=header, relief=tk.RIDGE)
            label.grid(row=0, column=col, sticky=tk.NSEW)

        # Populate the table with data
        for row_num, row_data in enumerate(rows, start=1):
            for col, value in enumerate(row_data):
                label = tk.Label(table, text=value, relief=tk.RIDGE)
                label.grid(row=row_num, column=col, sticky=tk.NSEW)

            # Create an "Edit" button to modify the data
            edit_button = tk.Button(table, text="Edit", command=lambda idx=row_data[0]: self.open_form(idx))
            edit_button.grid(row=row_num, column=len(row_data), sticky=tk.NSEW)

    def open_form(self, row_id):
        # Open the form for editing the selected row
        # You can implement your own logic here to open a form or dialog
        db = mysql.connector.connect(
            host='luca.werner.st',
            database='luca_SmartSchool',
            user='luca',
            password='lsgDbpw1!'
        )
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Routines WHERE ID = %s", (row_id,))
        row_data = cursor.fetchone()

        # Create a form to edit the data
        form = tk.Toplevel(self)
        form.title("Edit Form")

        # Labels
        labels = ["Name:", "Hours:", "Weekdays:", "Months:", "Temperature:"]
        for i, label_text in enumerate(labels):
            label = tk.Label(form, text=label_text)
            label.grid(row=i, column=0, sticky=tk.W)

        # Entry fields
        entry_texts = row_data[1:]  # Exclude ID column
        entry_vars = []
        for i, text in enumerate(entry_texts):  # Exclude Temperature column
            if i == 1:  # Hours column
                options = list(range(24))  # 0 - 23
                entry_var = tk.StringVar(value=', '.join(text))
                entry = tk.Listbox(form, selectmode="extended", exportselection=0)
                entry.grid(row=i, column=1, sticky=tk.W)
                for option in options:
                    entry.insert(tk.END, option)
                selected_options = [int(x) for x in text]
                #print(selected_options)
                ActiveHours = []
                HoursActive = []
                for x in selected_options:
                    #print (x)
                    #ActiveHours.append(x)
                    HoursActive.append(str(selected_options[x-1]))
                #print(ActiveHours)
                #print(selected_options)
                #print("selected options length: " + str(len(selected_options)))
                #print(HoursActive)
                #print("selectedoptions length: " + str(len(HoursActive)))
                global HA
                HA = ','.join(HoursActive)
                #print(HA)
                for option in selected_options:
                    index = options.index(option)
                    entry.select_set(index)
            elif i == 2:  # Weekdays column
                options = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                entry_var = tk.StringVar(value=', '.join(text))
                entry = tk.Listbox(form, selectmode="extended", exportselection=0)
                entry.grid(row=i, column=1, sticky=tk.W)
                for option in options:
                    entry.insert(tk.END, option)

                selected_options = [x for x in text]
                #print(selected_options)
                global DaysActive
                DaysActive = ','.join(selected_options)
                #print(DaysActive)
                for option in selected_options:
                    index = options.index(option)
                    entry.select_set(index)
            elif i == 3:  # Months column
                options = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
                           "October", "November", "December"]
                entry_var = tk.StringVar(value=', '.join(text))
                entry = tk.Listbox(form, selectmode="extended", exportselection=0)
                entry.grid(row=i, column=1, sticky=tk.W)
                for option in options:
                    entry.insert(tk.END, option)
                selected_options = [x for x in text]
                global MonthsActive
                MonthsActive = ','.join(selected_options)
                #print(MonthsActive)
                for option in selected_options:
                    index = options.index(option)
                    entry.select_set(index)

            else:
                entry_var = tk.StringVar(value=text)
                entry = tk.Entry(form, textvariable=entry_var)

            entry.grid(row=i, column=1, sticky=tk.W)
            entry_vars.append(entry_var)
            # Save button
            save_button = tk.Button(form, text="Save", command=lambda: self.save_data(db, row_id, entry_vars))
            save_button.grid(row=len(labels), columnspan=2, pady=10)








    def save_data(self, db, row_id, entry_vars):
        # Update the data in the database
        cursor = db.cursor()
        #query = "UPDATE Routines SET Name = %s, HoursActive = %s, DaysActive = %s, MonthsActive = %s, Temperature = %s WHERE ID = %s"
        values = []
        #query = "UPDATE Routines SET Name = %s, HoursActive = "+str(HA)+", DaysActive = "+str(DaysActive)+", MonthsActive = "+str(MonthsActive)+", Temperature = %s WHERE ID = %s"
        for var in entry_vars:
            value = var.get()

            if isinstance(value, (list, tuple)):
                # Convert list or tuple to comma-separated string
                value = ', '.join(str(item) for item in value)
            elif isinstance(value, float):
                # Round float value to 1 decimal place
                value = round(value, 1)
            elif isinstance(value, str):
                # Remove leading/trailing whitespace from string values
                value = value.strip()

            values.append(value)

        values.append(row_id)
        #cursor.execute(query, tuple(values))
        db.commit()

        messagebox.showinfo("Success", "Data updated successfully!")

        # Close the form after saving
        self.destroy()


        testmonths = MonthsActive
        print(testmonths)
        print(DaysActive)
        print(HA)


if __name__ == "__main__":
    app = DataEditor()
    app.mainloop()

"""
            elif i == 4:  # Temperature column
                entry_var = tk.DoubleVar(value=float(text))
                entry = tk.Spinbox(form, from_=0, to=100, increment=0.1, textvariable=entry_var)
                entry.grid(row=i, column=1, sticky=tk.NSEW)
"""