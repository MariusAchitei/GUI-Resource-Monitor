import customtkinter
import tkinter as tk


class ScrollableInfoFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.items = []

        for row, (key, value) in enumerate(item_list):
            self.add_item(row, key, value)

    def add_item(self, row, key, value):
        key_label = customtkinter.CTkLabel(self, text=key, width=20, anchor="w")
        value_label = customtkinter.CTkLabel(self, text=value, width=20, anchor="w")

        key_label.grid(row=row, column=0, padx=10, sticky="w")
        value_label.grid(row=row, column=1, padx=10, sticky="w")
