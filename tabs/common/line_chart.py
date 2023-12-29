import matplotlib.pyplot as plt
import mplcyberpunk
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class LineChart:
    def __init__(self, root, update_function, effects):
        self.root = root
        self.update_function = update_function
        self.effects = effects
        self.usage = []
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()

        self.bar = ttk.Progressbar(root, style="modern.Horizontal.TProgressbar", orient="horizontal",
                                   length=200, mode="determinate")
        self.bar.pack(pady=30)

        self.label = tk.Label(root, text='0%', bg='white')
        self.label.place(in_=self.bar, relx=1.0, x=20, rely=0)  # Adjust the position as neede
        self.update_line_chart()

    def update_line_chart(self):
        value = self.update_function()
        self.bar['value'] = value
        self.usage.append(value)
        self.ax.clear()
        self.ax.set_ylim(0, 100)
        self.ax.plot(self.usage)
        self.effects(self.ax)
        self.ax.set_title("CPU Usage")
        self.canvas.draw()

        self.label['text'] = f'{value}%'

        # Actualizează graficul la fiecare secundă
        self.root.after(1000, self.update_line_chart)
