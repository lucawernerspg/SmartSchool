from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
import mysql.connector
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from tkinter import *
import os
from kivymd.uix.button import MDRectangleFlatButton

def open_file():
    os.system('updateDB.py')



class Example(MDApp):
    def dbconnect(self):
        try:
            connection = mysql.connector.connect( host='luca.werner.st',
    database='luca_SmartSchool',
    user='luca',
    password='lsgDbpw1!')

            sql_select_Query = "SELECT * FROM Rooms"
            cursor = connection.cursor()
            cursor.execute(sql_select_Query)

            # get all records
            records = cursor.fetchall()
            data = []
            for row in records:
                datastring = row[0] , str(row[1]), str(row[2]) , str(row[3],)
                #print(row[0])
                btn = MDRectangleFlatButton(text="Update", on_release=lambda value=row[0]: open_file(value))
                #data.append(datastring + (btn,))
                data.append(datastring)
            return data


        except mysql.connector.Error as e:
            print("Error reading data from MySQL table", e)
        finally:
            if connection.is_connected():
                connection.close()
                cursor.close()
                print("MySQL connection is closed")

        for i in data:
            print(data[i])
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"

        # Call the dbconnect method to retrieve data
        row_data = self.dbconnect()

        layout = AnchorLayout()
        data_tables = MDDataTable(
            size_hint=(0.9, 0.6),
            use_pagination=True,
            column_data=[
                ("Name", dp(20)),
                ("Heaters", dp(20), ),
                ("Windows", dp(20), ),
                ("Capacity", dp(20), ),
                #("Change", dp(20)),
            ],
            row_data=row_data,
        )
        layout.add_widget(data_tables)
        return layout

    def sort_on_col_3(self, data):
        return zip(
            *sorted(
                enumerate(data),
                key=lambda l: l[1][3]
            )
        )

    def sort_on_col_2(self, data):
        return zip(
            *sorted(
                enumerate(data),
                key=lambda l: l[1][-1]
            )
        )
    def sort_on_col_4(self, data):
        return zip(
            *sorted(
                enumerate(data),
                key=lambda l: l[1][-1]
            )
        )

Example().run()