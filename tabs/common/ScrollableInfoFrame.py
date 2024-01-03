import customtkinter
import tkinter as tk

from utils.general_utils import string_to_float


class ScrollableInfoFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, enable_progress_bar=False, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.key_labels = []
        self.value_labels = []
        self.progress_bars = []
        self.items = []
        self.enable_progress_bar = enable_progress_bar

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

    def update_items(self, item_list):
        for row, (key, value) in enumerate(item_list):
            self.update_item(row, key, value)

    def update_item(self, row, key, value):
        self.key_labels[row].configure(text=key)
        self.value_labels[row].configure(text=value)
        if self.enable_progress_bar:
            # self.progress_bars[row].configure()
            self.progress_bars[row].set(string_to_float(value) / 100)
