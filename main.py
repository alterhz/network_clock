import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime
import subprocess
import pickle
from babel import numbers

import timer


# Function to load cached time data
def load_time_cache():
    try:
        with open('time_cache.pkl', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return [datetime.now().strftime("%H:%M:%S") for _ in range(3)]


# Function to save time data to cache
def save_time_cache():
    with open('time_cache.pkl', 'wb') as f:
        pickle.dump([time_var.get() for time_var in time_vars], f)


def set_date():
    selected_date_str = calendar.get_date()
    selected_date_obj = datetime.strptime(selected_date_str, "%m/%d/%y").date()  # Modified format
    date = selected_date_obj.strftime("%Y/%m/%d")
    set_str_date(date)


def set_str_date(date: str):
    """
    Set the system date to the selected date
    :param date: The selected date in YYYY/MM/DD format
    :return:
    """
    try:
        subprocess.run(['date', date], shell=True)  # Modified format
        status_label.config(text="System date updated successfully!")
    except Exception as e:
        status_label.config(text="Error: " + str(e))


def set_str_time(selected_time: str):
    """
    Set the system time to the selected time
    :param selected_time: The selected time in HH:MM:SS format
    :return:
    """
    try:
        subprocess.run(['time', selected_time], shell=True)
        status_label.config(text="System time updated successfully!")
    except Exception as e:
        status_label.config(text="Error: " + str(e))


def add_time_entry():
    time_vars.append(tk.StringVar(value=datetime.now().strftime("%H:%M:%S")))
    label = tk.Label(root, text="Time {}: ".format(len(time_vars)))
    row = len(time_vars) + 3
    label.grid(row=row, column=0, padx=(10, 0), pady=(5, 0))
    entry = ttk.Entry(root, textvariable=time_vars[-1])
    entry.grid(row=row, column=1, padx=(10, 0), pady=(0, 5))
    button = tk.Button(root, text="Set Time", command=lambda: set_str_time(time_vars[-1].get()))
    button.grid(row=row, column=2, padx=(10, 0), pady=(0, 5))


def set_network_time():
    network_time = timer.get_network_time()
    if network_time:
        set_str_date(network_time.strftime("%Y/%m/%d"))
        set_str_time(network_time.strftime("%H:%M:%S"))
    else:
        status_label.config(text="Error fetching network time")


def show_about_dialog():
    messagebox.showinfo("About", "System Date & Time Setter\nVersion 1.0\nDeveloped by Your Name")


# Create main window
root = tk.Tk()
root.title("系统日期和时间设置器")
# Set window size
root.geometry("800x600")

# Create menu bar
menubar = tk.Menu(root)
root.config(menu=menubar)

# Create a "File" menu
file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Network Timer", command=lambda: timer.main())
file_menu.add_command(label="Exit", command=lambda: on_closing())

# Create a "Help" menu
help_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=show_about_dialog)

set_network_time_button = tk.Button(root, text="Network Timer", command=timer.main, background="green")
set_network_time_button.grid(row=0, column=0, padx=(10, 0), pady=(10, 0))

# Create calendar
calendar = Calendar(root, selectmode='day', year=datetime.now().year, month=datetime.now().month,
                    day=datetime.now().day)
calendar.grid(row=0, column=1, padx=(10, 0), pady=(10, 0))

# Create button to set date
set_date_button = tk.Button(root, text="Set Date", command=set_date)
set_date_button.grid(row=0, column=2, padx=(10, 0), pady=(10, 0))

# 使用timer.get_network_time()，网络日期和时间设置本地日期和时间
# 请注意，这将需要管理员权限
set_network_time_button = tk.Button(root, text="Set Network Time", command=set_network_time, fg="red")
set_network_time_button.grid(row=0, column=3, padx=(10, 0), pady=(10, 0))

# Status label
status_label = tk.Label(root, text="")
status_label.grid(row=1, column=0, columnspan=3, padx=(10, 0), pady=(10, 0))

# Button to add more time entries
add_time_button = tk.Button(root, text="Add Time", command=add_time_entry)
add_time_button.grid(row=2, column=0)

# Load cached time data or use current time as default
time_vars = [tk.StringVar(value=time) for time in load_time_cache()]
time_labels = ["Time {}: ".format(i) for i in range(1, len(time_vars) + 1)]

# Create time selection entries and buttons in a single row
for i in range(len(time_vars)):
    row = i + 3
    label = tk.Label(root, text=time_labels[i])
    label.grid(row=row, column=0, padx=(10, 0), pady=(5, 0))
    entry = ttk.Entry(root, textvariable=time_vars[i])
    entry.grid(row=row, column=1, padx=(10, 0), pady=(0, 5))
    button = tk.Button(root, text="Set Time", command=lambda idx=i: set_str_time(time_vars[idx].get()))
    button.grid(row=row, column=2, padx=(10, 0), pady=(0, 5))


# Function to save time cache when the window is closed
def on_closing():
    save_time_cache()
    root.destroy()


# Configure the closing event
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
