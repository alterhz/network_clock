import tkinter as tk
from datetime import datetime, timedelta
import ntplib


def get_network_time():
    try:
        ntp_client = ntplib.NTPClient()
        # response = ntp_client.request('pool.ntp.org')
        # response = ntp_client.request('asia.pool.ntp.org')
        response = ntp_client.request('0.asia.pool.ntp.org')
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
    root.after(1000, update_time)  # 每秒钟更新一次时间显示


def refresh_network_time():
    global current_network_time
    network_time = get_network_time()
    if network_time:
        current_network_time = network_time
        time_label.config(text=network_time.strftime("%H:%M:%S"))
    root.after(60 * 1000, refresh_network_time)  # 每分钟获取一次网络时间


def change_opacity(value):
    opacity = max(float(value) / 100, 0.1)  # 将滑块值转换为透明度比例，确保最小值为0.1
    root.attributes("-alpha", opacity)  # 设置窗口透明度


root = tk.Tk()
root.title("当前时间")
root.wm_attributes("-topmost", True)  # 窗口置顶
root.attributes("-alpha", 0.8)  # 设置默认透明度为0.8

time_label = tk.Label(root, font=("Helvetica", 48), bg="black", fg="white")
time_label.pack(padx=20, pady=20)

current_network_time = get_network_time()  # 获取网络时间
if current_network_time:
    time_label.config(text=current_network_time.strftime("%H:%M:%S"))

refresh_button = tk.Button(root, text="刷新", command=refresh_network_time)
refresh_button.pack(pady=10)

# 创建一个IntVar对象并设置初始值为80
transparent = 80
opacity_var = tk.IntVar(value=transparent)
opacity_slider = tk.Scale(root, from_=1, to=100, orient=tk.HORIZONTAL, label="透明度", command=change_opacity,
                          variable=opacity_var)
opacity_slider.pack(pady=10)

change_opacity(transparent)

update_time()  # 启动每秒钟更新时间显示的函数
refresh_network_time()  # 启动每分钟获取网络时间的函数

root.mainloop()
