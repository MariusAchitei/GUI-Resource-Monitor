import os
from datetime import datetime

import customtkinter
import tkinter as tk
import csv

from utils.general_utils import string_to_float
from utils.general_utils import create_directory_if_not_exists


class ScrollableInfoFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, enable_progress_bar=False, enable_average=False, **kwargs):
        super().__init__(master, **kwargs)
        self.start_time = datetime.now()
        self.command = command
        self.key_labels = []
        self.value_labels = []
        self.progress_bars = []
        self.enable_progress_bar = enable_progress_bar
        self.enable_average = enable_average
        self.averages = []
        self.sum = []
        self.counts = []
        if enable_average:
            self.sum = [0] * len(item_list)
            self.counts = [0] * len(item_list)

        for row, (key, value) in enumerate(item_list):
            self.add_item(row, key, value)

    def add_item(self, row, key, value):
        key_label = customtkinter.CTkLabel(self, text=key, width=20, anchor="w")
        value_label = customtkinter.CTkLabel(self, text=value, width=20, anchor="w")

        key_label.grid(row=row, column=0, padx=10, sticky="w")
        value_label.grid(row=row, column=1, padx=10, sticky="w")

        self.key_labels.append(key_label)
        self.value_labels.append(value_label)

        if self.enable_progress_bar:
            progress_bar = customtkinter.CTkProgressBar(self, width=100, height=20, corner_radius=0)
            progress_bar.grid(row=row, column=2, padx=10, sticky="w")
            self.progress_bars.append(progress_bar)
        if self.enable_average:
            self.sum[row] = string_to_float(value)
            self.counts[row] += 1
            avg = round(self.sum[row] / self.counts[row], 2)
            average_label = customtkinter.CTkLabel(self, text=f'Average: {str(avg)}', width=20, anchor="w")
            average_label.grid(row=row, column=3, padx=10, sticky="w")
            self.averages.append(average_label)

    def update_items(self, item_list):
        for row, (key, value) in enumerate(item_list):
            self.update_item(row, key, value)

    def update_item(self, row, key, value):
        self.key_labels[row].configure(text=key)
        self.value_labels[row].configure(text=value)
        if self.enable_progress_bar:
            # self.progress_bars[row].configure()
            self.progress_bars[row].set(string_to_float(value) / 100)
        if self.enable_average:
            self.sum[row] += string_to_float(value)
            self.counts[row] += 1
            avg = round(self.sum[row] / self.counts[row], 2)
            self.averages[row].configure(text=f'Average: {str(avg)}')

    def save_state_as_csv(self, csv_file_path):
        # create_directory_if_not_exists(csv_file_path)
        os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
        file_exists = os.path.exists(csv_file_path)
        with open(csv_file_path, 'a+') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['start', 'end', 'elapsed_time'] + [label.cget('text') for label in self.key_labels])
            row = [datetime.now(), datetime.now() - self.start_time]
            if self.enable_average:
                row += [round(self.sum[row] / self.counts[row], 2) for row in range(0, len(self.sum))]
            else:
                row += [label.cget('text') for label in self.value_labels]
            writer.writerow(row)

    def get_state(self):
        return {
            "start_time": self.start_time,
            "key_labels": [label.cget('text') for label in self.key_labels],
            "value_labels": [label.cget('text') for label in self.value_labels],
            "progress_bars": [bar.get() for bar in self.progress_bars],
            "averages": [label.cget('text') for label in self.averages],
            "sum": self.sum,
            "counts": self.counts
        }

    def load_state(self, state):
        self.start_time = state['start_time']
        for row, key in enumerate(state['key_labels']):
            self.key_labels[row].configure(text=key)
        for row, value in enumerate(state['value_labels']):
            self.value_labels[row].configure(text=value)
        for row, value in enumerate(state['progress_bars']):
            self.progress_bars[row].set(value)
        for row, value in enumerate(state['averages']):
            self.averages[row].configure(text=value)
        self.sum = state['sum']
        self.counts = state['counts']
