import csv
import os
from datetime import datetime
import customtkinter
import matplotlib.pyplot as plt

from tabs.common.base_chart import BaseChart
from utils.general_utils import choose_equidistant_timestamps, seconds2human, get_current_date_time, \
    create_directory_if_not_exists

NUMBER_OF_TIMESTAMPS = 8


def save_plot():
    plt.savefig('')


class LineChart(BaseChart):
    def __init__(self, root, update_function, effects=lambda x: (), y_limit=(0, 100),
                 y_label_function=lambda x: f'{x}%',
                 dinamic_y_limit=False, self_update=True, title="Usage",
                 screenshot_path='screenshots/other', state=None):
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
        if state is not None:
            self.load_state(state)
            return
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

    def get_state(self):
        return {
            'start_time': self.start_time,
            'usage': self.usage,
            'max_usage': self.max_usage,
            'y_limit': self.y_limit,
            'sum': self.sum,
            'update_function': self.update_function,
            'effects': self.effects,
            'self_update': self.self_update,
            'title': self.title,
            # 'y_label_function': self.y_label_function,
            'dinamic_y_limit': self.dinamic_y_limit,
            'screenshot_path': self.screenshot_path
        }

    def load_state(self, state):
        self.start_time = state['start_time']
        self.usage = state['usage']
        self.max_usage = state['max_usage']
        self.y_limit = state['y_limit']
        self.sum = state['sum']
        self.update_function = state['update_function']
        self.effects = state['effects']
        self.self_update = state['self_update']
        self.title = state['title']
        # self.y_label_function = state['y_label_function']
        self.dinamic_y_limit = state['dinamic_y_limit']
        self.screenshot_path = state['screenshot_path']
        self.self_update = False
        # self.update_line_chart()
        return self
