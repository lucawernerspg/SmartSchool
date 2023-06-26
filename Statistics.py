import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import pandas as pd
import mysql.connector

canvas = None
# Function to calculate the date range based on user selection
def calculate_date_range(duration):
    end_date = datetime.now()
    if duration == "1 day":
        start_date = end_date - timedelta(days=1)
    elif duration == "1 week":
        start_date = end_date - timedelta(weeks=1)
    elif duration == "1 month":
        start_date = end_date - timedelta(days=30)
    elif duration == "1 year":
        start_date = end_date - timedelta(days=365)
    elif duration == "everything":
        # Set a very old start date to retrieve all entries
        start_date = datetime(1900, 1, 1)
    elif duration == "today":
        start_date = datetime.combine(datetime.today(), datetime.min.time())
    else:
        # Invalid duration selected
        messagebox.showerror("Error", "Invalid duration selected.")
        return None
    return start_date, end_date

# Function to fetch data from the database
def fetch_data():
    duration = duration_var.get()
    date_range = calculate_date_range(duration)
    if date_range is not None:
        try:
            # Connect to the MySQL database
            connection = mysql.connector.connect(
                host='luca.werner.st',
                database='luca_SmartSchool',
                user='luca',
                password='lsgDbpw1!'
            )

            # Query the database with the date range and retrieve the entries
            query = "SELECT Date, Temperature FROM Weather WHERE Date BETWEEN %s AND %s"
            start_date, end_date = date_range
            params = (start_date, end_date)
            cursor = connection.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()

            # Process the retrieved data
            dates = []
            values = []
            for row in results:
                dates.append(row[0])
                values.append(row[1])

            # Generate the graph
            generate_graph(dates, values)

        except mysql.connector.Error as error:
            messagebox.showerror("Error", str(error))

        finally:
            # Close the database connection
            if connection.is_connected():
                cursor.close()
                connection.close()

# Function to generate the graph
def generate_graph(dates, values):
    global canvas  # Use the global keyword to update the global variable

    fig, ax = plt.subplots()
    ax.plot(dates, values, color='blue', marker='o', linestyle='-', markersize=5)

    # Add a trendline
    trendline = pd.Series(values).rolling(window=3).mean()
    ax.plot(dates, trendline, color='red', linestyle='--', label='Trendline')

    if duration_var.get() == "today":
        # Set the x-axis format to display only hours and minutes
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda value, _: pd.to_datetime(value).strftime('%H:%M')))
    else:
        # Set the x-axis format to display the start and end dates
        start_date = pd.to_datetime(dates[0]).strftime('%Y-%m-%d')
        end_date = pd.to_datetime(dates[-1]).strftime('%Y-%m-%d')
        ax.set_xlabel(f'Date ({start_date} - {end_date})')

        # Remove the intermediate dates from the x-axis
        ax.set_xticks([dates[0], dates[-1]])

    ax.set_ylabel('Value')
    ax.set_title('Data Graph')

    # Configure the legend
    ax.legend()

    # If the canvas exists, delete it before creating a new one
    if canvas is not None:
        canvas.get_tk_widget().destroy()

    # Embed the graph in the GUI
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Update the x-axis tick labels for "today" option
    if duration_var.get() == "today":
        ax.set_xticklabels([pd.to_datetime(date).strftime('%H:%M') for date in dates])


# Create the GUI window
window = tk.Tk()
window.title("Data Graph")

# Create a dropdown menu to select the duration
duration_var = tk.StringVar(window)
duration_choices = ["today","1 day", "1 week", "1 month", "1 year", "everything"]
duration_var.set(duration_choices[0])
duration_dropdown = tk.OptionMenu(window, duration_var, *duration_choices)
duration_dropdown.pack()

# Create a button to fetch data and generate the graph
fetch_button = tk.Button(window, text="Fetch Data", command=fetch_data)
fetch_button.pack()

# Create a placeholder for the graph canvas
canvas = None

# Start the GUI main loop
window.mainloop()