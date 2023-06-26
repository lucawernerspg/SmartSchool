import tkinter as tk
import threading
import subprocess

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Script Navigator")
        self.geometry("800x600")
        self.create_navigation_bar()
        self.create_script_frame()

    def create_navigation_bar(self):
        self.navigation_bar = tk.Frame(self)
        self.navigation_bar.pack(side=tk.TOP, fill=tk.X)

        # Create buttons for each script
        scripts = [
            {"name": "Script 1", "function": self.run_script1},
            {"name": "Script 2", "function": self.run_script2},
            {"name": "Script 3", "function": self.run_script3}
        ]
        self.script_buttons = []
        for script in scripts:
            button = tk.Button(self.navigation_bar, text=script["name"], command=script["function"])
            button.pack(side=tk.LEFT)
            self.script_buttons.append(button)

    def create_script_frame(self):
        self.script_frame = tk.Frame(self)
        self.script_frame.pack(fill=tk.BOTH, expand=True)

    def run_script1(self):
        self.run_script("GUIAirTest.py")

    def run_script2(self):
        self.run_script("GUIupdateDBTest.py")

    def run_script3(self):
        self.run_script("Statistics.py")

    def run_script(self, file):
        # Destroy the existing script frame
        self.script_frame.destroy()
        self.create_script_frame()

        # Create a new thread to run the script
        thread = threading.Thread(target=self.execute_script, args=(file,))
        thread.start()

    def execute_script(self, file):
        script_process = subprocess.Popen(["python", file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = script_process.communicate()

        # Display the script output/error in a text widget
        text_widget = tk.Text(self.script_frame)
        text_widget.pack(fill=tk.BOTH, expand=True)

        if output:
            text_widget.insert(tk.END, output.decode("utf-8"))
        elif error:
            text_widget.insert(tk.END, error.decode("utf-8"))
        else:
            text_widget.insert(tk.END, "Script execution completed.")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
