import tkinter as tk
from tkinter import ttk
import psutil
import matplotlib.pyplot as plt
import mplcyberpunk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import os

mplcyberpunk.add_glow_effects()

plt.style.use("cyberpunk")

# Clasa pentru aplicația GUI
class SystemMonitorApp:
    def __init__(self, root):
        self.root = root
        root.title("System Monitor")

        # Crearea tab-urilor pentru diferite resurse
        tabControl = ttk.Notebook(root)
        self.cpu_tab = ttk.Frame(tabControl)
        self.memory_tab = ttk.Frame(tabControl)
        # Alte tab-uri pot fi adăugate aici

        tabControl.add(self.cpu_tab, text='CPU')
        tabControl.add(self.memory_tab, text='Memory')
        # Alte tab-uri pot fi adăugate aici

        tabControl.pack(expand=1, fill="both")

        # Inițializarea graficelor și datelor
        self.init_cpu_tab()
        self.init_memory_tab()
        # Alte inițializări pot fi adăugate aici

    def init_cpu_tab(self):
        self.cpu_usage = []
        self.cpu_fig, self.cpu_ax = plt.subplots()
        self.cpu_canvas = FigureCanvasTkAgg(self.cpu_fig, master=self.cpu_tab)
        self.cpu_canvas.get_tk_widget().pack()

        self.cpu_bar = ttk.Progressbar(self.cpu_tab, style="modern.Horizontal.TProgressbar", orient="horizontal",
                                      length=200, mode="determinate")
        self.cpu_bar.pack(pady=30)


        self.cpu_label = tk.Label(self.cpu_tab, text='0%', bg='white')
        self.cpu_label.place(in_=self.cpu_bar, relx=1.0, x=20, rely=0)  # Adjust the position as neede

        self.update_cpu_usage()

    def init_memory_tab(self):
        self.memory_usage = []
        self.memory_fig, self.memory_ax = plt.subplots()
        self.memory_canvas = FigureCanvasTkAgg(self.memory_fig, master=self.memory_tab)
        self.memory_canvas.get_tk_widget().pack()

        self.memory_bar = ttk.Progressbar(self.memory_tab, style="modern.Horizontal.TProgressbar", orient="horizontal",
                                  length=200, mode="determinate")
        self.memory_bar.pack(pady=30)

        self.memory_label = tk.Label(self.memory_tab, text='0%', bg='white')
        self.memory_label.place(x=100, y=25)  # Adjust the position as needed

        self.update_memory_usage()

    def update_cpu_usage(self):
        cpu_percent = psutil.cpu_percent()
        self.cpu_bar['value'] = cpu_percent
        self.cpu_usage.append(cpu_percent)
        self.cpu_ax.clear()
        self.cpu_ax.set_ylim(0, 100)
        self.cpu_ax.plot(self.cpu_usage, marker='o')
        mplcyberpunk.add_glow_effects()
        self.cpu_ax.set_title("CPU Usage")
        self.cpu_canvas.draw()

        self.cpu_label['text'] = f'{cpu_percent}%'

        # Actualizează graficul la fiecare secundă
        self.root.after(1000, self.update_cpu_usage)

    def update_memory_usage(self):
        memory = psutil.virtual_memory()
        self.memory_bar['value'] = memory.percent
        self.memory_usage.append(memory.percent)
        self.memory_ax.clear()
        self.memory_ax.set_ylim(0, 100)
        self.memory_ax.plot(self.memory_usage, marker='o')
        mplcyberpunk.add_glow_effects()
        self.memory_ax.set_title("Memory Usage")
        self.memory_canvas.draw()

        self.memory_label['text'] = f'{memory.percent}%'

        # Actualizează graficul la fiecare secundă
        self.root.after(1000, self.update_memory_usage)


# Rularea aplicației
root = tk.Tk()

style = ttk.Style(root)
style.theme_use('clam')  # Use a modern theme

# Customize the style of the progress bar
style.configure("modern.Horizontal.TProgressbar", troughcolor='gray',
                bordercolor='gray', background='green', lightcolor='green', darkcolor='green')

app = SystemMonitorApp(root)
root.mainloop()
