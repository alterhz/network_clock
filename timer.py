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


class NetworkTimeApp:
    def __init__(self, master):
        self.master = master
        master.title("当前网络时间")
        master.wm_attributes("-topmost", True)
        master.attributes("-alpha", 0.8)

        # 日期
        self.date_label = tk.Label(master, font=("Helvetica", 16), bg="black", fg="white")
        self.date_label.pack(padx=1, pady=1)
        # 时间
        self.time_label = tk.Label(master, font=("Helvetica", 48), bg="black", fg="green")
        self.time_label.pack(padx=20)

        self.current_network_time = get_network_time()
        if self.current_network_time:
            self.time_label.config(text=self.current_network_time.strftime("%H:%M:%S"))

        self.refresh_button = tk.Button(master, text="刷新", command=self.refresh_network_time)
        self.refresh_button.pack(pady=10, ipadx=10)

        transparent = 80
        self.opacity_var = tk.IntVar(value=transparent)
        self.opacity_slider = tk.Scale(master, from_=1, to=100, orient=tk.HORIZONTAL, label="透明度",
                                       command=self.change_opacity, variable=self.opacity_var)
        self.opacity_slider.pack(pady=10)

        self.change_opacity(transparent)

        self.update_time()
        self.refresh_network_time()

        self.window_hidden = False
        self.toggle_button = tk.Button(master, text="隐藏窗口", command=self.toggle_window)
        self.toggle_button.pack(pady=10)

    def update_time(self):
        if self.current_network_time:
            self.current_network_time += timedelta(seconds=1)
            current_time = self.current_network_time.strftime("%H:%M:%S")
            self.time_label.config(text=current_time)
        self.master.after(1000, self.update_time)

    def refresh_network_time(self):
        network_time = get_network_time()
        if network_time:
            self.current_network_time = network_time
            self.date_label.config(text=network_time.strftime("%Y年%m月%d日"))
            self.time_label.config(text=network_time.strftime("%H:%M:%S"))
            self.time_label.config(fg="red")
            self.master.after(2000, lambda: self.time_label.config(fg="green"))  # Change back to green after 2 seconds
        self.master.after(10000, self.refresh_network_time)  # Refresh network time every 10 seconds

    def change_opacity(self, value):
        opacity = max(float(value) / 100, 0.1)
        self.master.attributes("-alpha", opacity)

    def toggle_window(self):
        self.window_hidden = not self.window_hidden
        if self.window_hidden:
            self.master.overrideredirect(True)
            self.master.grab_set()  # Make the window non-interactive
            self.refresh_button.pack_forget()
            self.opacity_slider.pack_forget()
            self.toggle_button.config(text="显示窗口")
        else:
            self.master.overrideredirect(False)
            self.master.grab_release()  # Release the grab, allowing interaction
            self.refresh_button.pack(pady=10)
            self.opacity_slider.pack(pady=10)
            self.toggle_button.config(text="隐藏窗口")


def main():
    root = tk.Tk()
    app = NetworkTimeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
