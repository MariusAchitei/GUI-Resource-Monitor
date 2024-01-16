import csv
import os
from datetime import datetime
import customtkinter
import matplotlib.pyplot as plt
import mplcyberpunk
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from tabs.common.base_chart import BaseChart
from utils.general_utils import choose_equidistant_timestamps, seconds2human, get_current_date_time, \
    create_directory_if_not_exists

NUMBER_OF_TIMESTAMPS = 8


def save_plot():
    plt.savefig('')


class LineChart(BaseChart):
    def __init__(self, root, update_function, effects=lambda x: (), y_limit=(0, 100), y_label_function=lambda x: x,
                 dinamic_y_limit=False, self_update=True, title="Usage",
                 screenshot_path='screenshots/other'):
        super().__init__(root)
        self.start_time = datetime.now()
        self.update_function = update_function
        self.effects = effects
        self.self_update = self_update
        self.screenshot_path = screenshot_path
        self.title = title
        self.usage = []
        self.max_usage = 0
        self.y_label_function = y_label_function
        self.dinamic_y_limit = dinamic_y_limit
        self.y_limit = y_limit
        self.sum = 0

        self.bar = customtkinter.CTkProgressBar(root, width=200, height=20, corner_radius=0)
        self.bar.pack(pady=30)

        self.label = customtkinter.CTkLabel(root, text='0%', width=20, anchor="w")
        self.label.place(in_=self.bar, relx=1.0, x=20, rely=0)

        self.avg_label = customtkinter.CTkLabel(root, text='Average: 0', width=20, anchor="w")
        self.avg_label.pack(pady=10)

        if self_update:
            self.update_line_chart()

    def update_line_chart(self):
        value = self.update_function()
        self.sum += value
        if self.max_usage < value:
            self.max_usage = value
            if self.dinamic_y_limit:
                self.y_limit = (self.y_limit[0], self.max_usage)
        self.bar.set(value / self.y_limit[1])
        self.usage.append(value)
        self.ax.clear()
        self.ax.set_ylim(self.y_limit[0], self.y_limit[1])
        self.ax.plot(self.usage)
        self.ax.set_ylabel('Usage')
        self.ax.set_xlabel('Time')

        labels = [label.get_position()[1] for label in self.ax.get_yticklabels()]
        y_labels = list(map(self.y_label_function, labels))

        self.ax.set_yticks(self.ax.get_yticks())
        self.ax.set_yticklabels(y_labels)

        timestamps = choose_equidistant_timestamps(len(self.usage), NUMBER_OF_TIMESTAMPS)
        x_ticks = [i for i, timestamp in enumerate(self.usage) if timestamp in timestamps]
        x_labels = [seconds2human(timestamp) for timestamp in timestamps]

        self.ax.set_xticks(timestamps)
        self.ax.set_xticklabels(x_labels)

        self.effects(self.ax)
        self.ax.set_title(self.title)
        self.canvas.draw()

        avg = round(self.sum / len(self.usage), 2)
        if self.y_limit[0] == 0 and self.y_limit[1] == 100:
            self.label.configure(text=f"{value}%")
            self.avg_label.configure(text=f'Average: {avg}%')
        else:
            self.label.configure(text=f"{self.y_label_function(value)} / {self.y_label_function(self.y_limit[1])}")
            self.avg_label.configure(
                text=f'Average: {self.y_label_function(avg)}')

        if self.self_update:
            self.root.after(1000, self.update_line_chart)

    def get_max_value(self):
        return self.max_usage

    def get_current_value(self):
        return self.usage[-1]

    def save_state_as_csv(self, csv_file_path):
        create_directory_if_not_exists(csv_file_path)
        file_exists = os.path.exists(csv_file_path)
        with open(csv_file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['start', 'end', 'elapsed_time', 'average'])
            writer.writerow([self.start_time.strftime("%d/%m/%Y %H:%M:%S"),
                             datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                             str(datetime.now() - self.start_time),
                             str(round(self.sum / len(self.usage), 2))])
