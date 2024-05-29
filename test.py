import tkinter as tk
from datetime import datetime, timedelta
import ntplib

def get_network_time():
    try:
        ntp_client = ntplib.NTPClient()
        response = ntp_client.request('time.windows.com')
        network_time = datetime.fromtimestamp(response.tx_time)
        return network_time
    except Exception as e:
        print("Error fetching network time:", e)
        return None

def update_time():
    global current_network_time
    if current_network_time:
        current_network_time += timedelta(seconds=1)
        current_time = current_network_time.strftime("%H:%M:%S")
        time_label.config(text=current_time)
    root.after(1000, update_time)

def refresh_network_time():
    global current_network_time
    network_time = get_network_time()
    if network_time:
        current_network_time = network_time
        time_label.config(text=network_time.strftime("%H:%M:%S"))
        time_label.config(fg="red")
        root.after(2000, lambda: time_label.config(fg="green"))  # Change back to green after 2 seconds
    root.after(10000, refresh_network_time)  # Refresh network time every 10 seconds

def change_opacity(value):
    opacity = max(float(value) / 100, 0.1)
    root.attributes("-alpha", opacity)

def pass_through_click(event):
    x, y = event.x_root, event.y_root
    root.event_generate('<Button-1>', x=x, y=y, time=event.time)

root = tk.Tk()
root.title("当前时间")
root.wm_attributes("-topmost", True)
root.attributes("-alpha", 0.5)  # Set initial transparency to 0 (fully transparent)
root.overrideredirect(True)  # Remove window decorations
root.geometry("+0+0")  # Move the window to the top left corner

time_label = tk.Label(root, font=("Helvetica", 48), bg="black", fg="green")
time_label.pack(padx=20, pady=20)

current_network_time = get_network_time()
if current_network_time:
    time_label.config(text=current_network_time.strftime("%H:%M:%S"))

update_time()
refresh_network_time()

root.bind('<Button-1>', pass_through_click)  # Bind left click event to pass_through_click function

root.mainloop()
