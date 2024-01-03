import customtkinter
import matplotlib.pyplot as plt
import mplcyberpunk
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from utils.general_utils import choose_equidistant_timestamps, seconds2human

NUMBER_OF_TIMESTAMPS = 8


class LineChart:
    def __init__(self, root, update_function, effects, y_limit=(0, 100), y_label_function=lambda x: x):
        self.root = root
        self.update_function = update_function
        self.effects = effects
        self.usage = []
        self.y_label_function = y_label_function
        self.y_limit = y_limit
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()

        self.bar = customtkinter.CTkProgressBar(root, width=200, height=20, corner_radius=0)
        # if y_limit[0] == 0 and y_limit[1] == 100:
        self.bar.pack(pady=30)

        # self.label = customtkinter.CTkLabel(root, text='0%', bg='white')
        self.label = customtkinter.CTkLabel(root, text='0%', width=20, anchor="w")
        self.label.place(in_=self.bar, relx=1.0, x=20, rely=0)  # Adjust the position as neede
        self.update_line_chart()

    def update_line_chart(self):
        value = self.update_function()
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
        self.ax.set_title("Usage")
        self.canvas.draw()

        if self.y_limit[0] == 0 and self.y_limit[1] == 100:
            self.label.configure(text=f"{value}%")
        else:
            self.label.configure(text=f"{self.y_label_function(value)} / {self.y_label_function(self.y_limit[1])}")

        self.root.after(1000, self.update_line_chart)
