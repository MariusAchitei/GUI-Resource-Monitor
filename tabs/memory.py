import customtkinter

from tabs.common.line_chart import LineChart
import matplotlib.pyplot as plt
import psutil
import mplcyberpunk


def init_memory(root):
    plt.style.use("cyberpunk")
    MemoryTab(root)


def memory_update_function():
    return psutil.virtual_memory().percent


class MemoryTab:
    def __init__(self, root):
        self.tabview = customtkinter.CTkTabview(root, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("info")
        self.tabview.add("usage")
        self.tabview.tab("info").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("usage").grid_columnconfigure(0, weight=1)

        LineChart(self.tabview.tab("usage"), memory_update_function, mplcyberpunk.add_glow_effects)
