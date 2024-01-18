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
    """
    Class used to create a very customisable line chart. It can be used to create a line chart that updates itself
    every second. It can be used to create a line chart that doesn't update itself.
    It has at his core a matplotlib figure and a matplotlib axes. It has a canvas that is used to display the figure.
    """

    def __init__(self, root, update_function, effects=lambda x: (), y_limit=(0, 100),
                 y_label_function=lambda x: f'{x}%',
                 dinamic_y_limit=False, self_update=True, title="Usage",
                 screenshot_path='screenshots/other'):
        """
        Initializes the line chart.
        :param root: Sets the root of the line chart.
        :param update_function: is the function that is called to update the line chart, every second.
        :param effects: used to customise the default style of the line chart (plt).
        :param y_limit: It can be procentual or absolute. It is used to set the y limit of the line chart.
        :param y_label_function: The value of the y axis is passed to this function to be converted to a value that will be shown on the figure ((x) to x% or x to x mb/s).
        :param dinamic_y_limit: If set to true, the y limit will be updated every time a new maximum value is found.
        :param self_update: If set to true, the line chart will update itself every second.
        :param title: The title of the line chart.
        :param screenshot_path: The path where the screenshots of the line chart will be saved.
        """
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
        """
        Updates the line chart.
        :return: void
        """
        # if len(self.usage) > 10:
        #     self.save_chart()
        #     self.reset()
        #     if self.self_update:
        #         self.root.after(1000, self.update_line_chart)
        #     return
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

        self.label.configure(text=f"{self.y_label_function(value)} / {self.y_label_function(self.y_limit[1])}")
        self.avg_label.configure(
            text=f'Average: {self.y_label_function(avg)}')

        if self.self_update:
            self.root.after(1000, self.update_line_chart)

    def reset(self):
        """
        Resets the line chart.
        :return: void
        """
        self.usage = []
        self.sum = 0
        self.max_usage = 0

    def get_max_value(self):
        """
        Returns the maximum value of the line chart.
        :return: the maximum value of the line chart
        """
        return self.max_usage

    def get_current_value(self):
        """
        Returns the current value of the line chart.
        :return: the current value of the line chart
        """
        return self.usage[-1]

    def save_state_as_csv(self, csv_file_path):
        """
        Saves the state of the line chart as a csv file.
        :param csv_file_path: the path where the csv file will be saved
        :return: void
        """
        # create_directory_if_not_exists(csv_file_path)
        os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
        file_exists = os.path.exists(csv_file_path)
        with open(csv_file_path, 'a+') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['start', 'end', 'elapsed_time', 'average'])
            avg = round(self.sum / len(self.usage), 2)
            time_diff = datetime.now() - self.start_time
            writer.writerow([self.start_time.strftime("%d/%m/%Y %H:%M:%S"),
                             datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                             str(time_diff),
                             self.y_label_function(avg)])
        self.reset()
