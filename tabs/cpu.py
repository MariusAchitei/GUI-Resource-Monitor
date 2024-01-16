import pickle

import customtkinter

from tabs.common.ScrollableInfoFrame import ScrollableInfoFrame
from tabs.common.base_tab import BaseTab
from tabs.common.line_chart import LineChart
import matplotlib.pyplot as plt
import mplcyberpunk

from utils.cpu_utils import *


def init_cpu(root):
    plt.style.use("cyberpunk")
    CpuTab(root)


class CpuTab(BaseTab):
    def __init__(self, root):
        super().__init__(root)
        self.screenshot_path = f'{self.screenshot_path}/cpu'
        self.export_path = f'{self.export_path}/cpu'
        self.state_path = f'{self.state_path}/cpu'
        self.tabview.add("info")
        self.tabview.add("usage")
        self.tabview.tab("info").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("usage").grid_columnconfigure(0, weight=1)
        self.populate_info()
        self.populate_usage()

    def populate_usage(self):
        self.usagetabview = customtkinter.CTkTabview(self.tabview.tab("usage"), width=self.width - 20,
                                                     height=self.height - 20)
        self.usagetabview.grid(row=0, column=2, sticky="nsew")
        self.usagetabview.add("general")
        self.usagetabview.add("per core")
        self.usagetabview.tab("general").grid_columnconfigure(0, weight=1)
        self.usagetabview.tab("per core").grid_columnconfigure(0, weight=1)
        self.chart = LineChart(self.usagetabview.tab("general"), update_cpu_function,
                               effects=mplcyberpunk.add_glow_effects,
                               screenshot_path=f'{self.screenshot_path}/usage',
                               title="CPU Usage")
        self.init_per_core_usage(self.usagetabview.tab("per core"))

    def populate_info(self):
        cpu_info = get_cpu_info()
        self.info_frame = ScrollableInfoFrame(master=self.tabview.tab("info"),
                                              command=None,
                                              item_list=cpu_info.items(), width=self.width - 20,
                                              height=self.height - 20)
        self.info_frame.grid(row=0, column=0, padx=15, pady=15, sticky="ns")

    def init_per_core_usage(self, parent):
        cpus = get_per_core_usage()
        self.per_core_usage = ScrollableInfoFrame(master=parent,
                                                  command=None,
                                                  item_list=cpus.items(),
                                                  width=self.width - 20,
                                                  height=self.height - 20,
                                                  enable_progress_bar=True,
                                                  enable_average=True)
        self.per_core_usage.grid(row=0, column=0, padx=15, pady=15, sticky="ns")
        self.update_per_core_usage()

    def update_per_core_usage(self):
        cpus = get_per_core_usage()
        self.per_core_usage.update_items(cpus.items())
        self.per_core_usage.after(1000, self.update_per_core_usage)

    def save_as_csv(self):
        self.chart.save_state_as_csv(f'{self.export_path}/usage.csv')
        self.per_core_usage.save_state_as_csv(f'{self.export_path}/per_core.csv')

    def get_state(self):
        return {
            "chart": self.chart.get_state(),
            "per_core_usage": self.per_core_usage.get_state(),
            "info_frame": self.info_frame.get_state()
        }

    def set_state(self, state):
        self.chart.load_state(state["chart"])
        self.per_core_usage.load_state(state["per_core_usage"])
        self.info_frame.load_state(state["info_frame"])
