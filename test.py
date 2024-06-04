import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar, DateEntry


class TimePicker(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("时间选择器示例")

        # 日期选择器
        self.date_label = tk.Label(self, text="选择日期:")
        self.date_label.grid(row=0, column=0, padx=10, pady=10)
        self.date_entry = DateEntry(self, width=12, background='darkblue',
                                    foreground='white', borderwidth=2, date_pattern='y-mm-dd')
        self.date_entry.grid(row=0, column=1, padx=10, pady=10)

        # 时间选择器
        self.time_label = tk.Label(self, text="选择时间:")
        self.time_label.grid(row=1, column=0, padx=10, pady=10)

        self.hour_var = tk.StringVar(value='00')
        self.hour_spinbox = tk.Spinbox(self, from_=0, to=23, wrap=True, textvariable=self.hour_var, width=3,
                                       format="%02.0f")
        self.hour_spinbox.grid(row=1, column=1, padx=(10, 0), pady=10, sticky='w')

        self.minute_var = tk.StringVar(value='00')
        self.minute_spinbox = tk.Spinbox(self, from_=0, to=59, wrap=True, textvariable=self.minute_var, width=3,
                                         format="%02.0f")
        self.minute_spinbox.grid(row=1, column=1, padx=(60, 0), pady=10, sticky='w')

        # 获取结果按钮
        self.get_button = tk.Button(self, text="获取选择的日期和时间", command=self.get_datetime)
        self.get_button.grid(row=2, column=0, columnspan=2, pady=10)

        # 显示结果
        self.result_label = tk.Label(self, text="")
        self.result_label.grid(row=3, column=0, columnspan=2, pady=10)

    def get_datetime(self):
        date = self.date_entry.get()
        hour = self.hour_var.get()
        minute = self.minute_var.get()
        datetime_str = f"选择的日期和时间: {date} {hour}:{minute}"
        self.result_label.config(text=datetime_str)


if __name__ == "__main__":
    app = TimePicker()
    app.mainloop()
