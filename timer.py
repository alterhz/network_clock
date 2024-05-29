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


def toggle_window():
    global window_hidden
    window_hidden = not window_hidden
    if window_hidden:
        root.overrideredirect(True)
        root.grab_set()  # Make the window non-interactive
        refresh_button.pack_forget()
        opacity_slider.pack_forget()
        toggle_button.config(text="显示窗口")
    else:
        root.overrideredirect(False)
        root.grab_release()  # Release the grab, allowing interaction
        refresh_button.pack(pady=10)
        opacity_slider.pack(pady=10)
        toggle_button.config(text="隐藏窗口")


root = tk.Tk()
root.title("当前时间")
root.wm_attributes("-topmost", True)
root.attributes("-alpha", 0.8)

time_label = tk.Label(root, font=("Helvetica", 48), bg="black", fg="green")
time_label.pack(padx=20, pady=20)

current_network_time = get_network_time()
if current_network_time:
    time_label.config(text=current_network_time.strftime("%H:%M:%S"))

refresh_button = tk.Button(root, text="刷新", command=refresh_network_time)
refresh_button.pack(pady=10)

transparent = 80
opacity_var = tk.IntVar(value=transparent)
opacity_slider = tk.Scale(root, from_=1, to=100, orient=tk.HORIZONTAL, label="透明度", command=change_opacity,
                          variable=opacity_var)
opacity_slider.pack(pady=10)

change_opacity(transparent)

update_time()
refresh_network_time()

window_hidden = False
toggle_button = tk.Button(root, text="隐藏窗口", command=toggle_window)
toggle_button.pack(pady=10)

root.mainloop()
