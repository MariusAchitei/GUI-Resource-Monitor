import customtkinter

from tabs.common.ScrollableInfoFrame import ScrollableInfoFrame
from tabs.common.line_chart import LineChart
import matplotlib.pyplot as plt
import mplcyberpunk

from utils.cpu_utils import *

WIDTH = 500
HEIGHT = 400


def init_cpu(root):
    plt.style.use("cyberpunk")
    CpuTab(root)


class CpuTab:
    def __init__(self, root):
        self.tabview = customtkinter.CTkTabview(root, width=WIDTH, height=HEIGHT)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("info")
        self.tabview.add("usage")
        self.tabview.tab("info").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("usage").grid_columnconfigure(0, weight=1)
        self.populate_info()
        self.populate_usage()

    def populate_usage(self):
        self.usagetabview = customtkinter.CTkTabview(self.tabview.tab("usage"), width=WIDTH - 20, height=HEIGHT - 20)
        self.usagetabview.grid(row=0, column=2, sticky="nsew")
        self.usagetabview.add("general")
        self.usagetabview.add("per core")
        self.usagetabview.tab("general").grid_columnconfigure(0, weight=1)
        self.usagetabview.tab("per core").grid_columnconfigure(0, weight=1)
        LineChart(self.usagetabview.tab("general"), update_cpu_function, effects=mplcyberpunk.add_glow_effects)
        self.init_per_core_usage(self.usagetabview.tab("per core"))

    def populate_info(self):
        cpu_info = get_cpu_info()
        self.info_frame = ScrollableInfoFrame(master=self.tabview.tab("info"),
                                              command=None,
                                              item_list=cpu_info.items(), width=WIDTH - 20,
                                              height=HEIGHT - 20)
        self.info_frame.grid(row=0, column=0, padx=15, pady=15, sticky="ns")

    def init_per_core_usage(self, parent):
        cpus = {}
        for index, percent in enumerate(list(get_per_core_usage())):
            cpus[f"cpu{index + 1}"] = percent
        self.per_core_usage = ScrollableInfoFrame(master=parent,
                                                  command=None,
                                                  item_list=cpus.items(),
                                                  width=WIDTH - 20,
                                                  height=HEIGHT - 20,
                                                  enable_progress_bar=True)
        self.per_core_usage.grid(row=0, column=0, padx=15, pady=15, sticky="ns")
        self.update_per_core_usage()

    def update_per_core_usage(self):
        cpus = {}
        for index, percent in enumerate(list(get_per_core_usage())):
            cpus[f"cpu{index + 1}"] = f"{percent}%"
        self.per_core_usage.update_items(cpus.items())
        self.per_core_usage.after(1000, self.update_per_core_usage)
