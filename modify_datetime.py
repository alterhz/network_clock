import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime
import subprocess
import pickle
# 注意：from babel import numbers，不然打包后运行会报错
from babel import numbers


# Function to load cached time data
def load_time_cache():
    try:
        with open('time_cache.pkl', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return [datetime.now().strftime("%H:%M:%S") for _ in range(5)]


# Function to save time data to cache
def save_time_cache():
    with open('time_cache.pkl', 'wb') as f:
        pickle.dump([time_var.get() for time_var in time_vars], f)


def set_date():
    selected_date_str = calendar.get_date()
    selected_date_obj = datetime.strptime(selected_date_str, "%m/%d/%y").date()  # Modified format
    date = selected_date_obj.strftime("%Y/%m/%d")
    try:
        subprocess.run(['date', date], shell=True)  # Modified format
        status_label.config(text="System date updated successfully!")
    except Exception as e:
        status_label.config(text="Error: " + str(e))


def set_time(time_var):
    selected_time = time_var.get()
    try:
        subprocess.run(['time', selected_time], shell=True)
        status_label.config(text="System time updated successfully!")
    except Exception as e:
        status_label.config(text="Error: " + str(e))


# Create main window
root = tk.Tk()
root.title("System Date & Time Setter")

# Create calendar
calendar = Calendar(root, selectmode='day', year=datetime.now().year, month=datetime.now().month,
                    day=datetime.now().day)
calendar.pack(padx=10, pady=10)

# Create button to set date
set_date_button = tk.Button(root, text="Set Date", command=set_date)
set_date_button.pack(pady=5)

# Load cached time data or use current time as default
time_labels = ["Time 1:", "Time 2:", "Time 3:", "Time 4:", "Time 5:"]
time_vars = [tk.StringVar(value=time) for time in load_time_cache()]

# Create time selection entries and buttons in a single row
for i in range(5):
    label = tk.Label(root, text=time_labels[i])
    label.pack(anchor="w", padx=(10, 0), pady=(5, 0))
    entry = ttk.Entry(root, textvariable=time_vars[i])
    entry.pack(anchor="w", padx=(10, 0), pady=(0, 5))
    button = tk.Button(root, text="Set Time", command=lambda idx=i: set_time(time_vars[idx]))
    button.pack(anchor="w", padx=(10, 0), pady=(0, 10))

# Status label
status_label = tk.Label(root, text="")
status_label.pack(pady=(10, 0))


# Function to save time cache when the window is closed
def on_closing():
    save_time_cache()
    root.destroy()


# Configure the closing event
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
