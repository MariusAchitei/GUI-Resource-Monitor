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
    """
    Class used to create the CPU tab. It inherits from BaseTab. It has 2 tabs: info and usage.
    """

    def __init__(self, root):
        """
        Initializes the CPU tab. It creates the 2 tabs: info and usage.
        It also creates the line chart that is used to display the CPU usage.
        It also creates the ScrollableInfoFrame that is used to display the CPU info.
        param root: the root of the tab.
        """
        super().__init__(root)
        self.screenshot_path = f'{self.screenshot_path}/cpu'
        self.export_path = f'{self.export_path}/cpu'
        self.tabview.add("info")
        self.tabview.add("usage")
        self.tabview.tab("info").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("usage").grid_columnconfigure(0, weight=1)
        self.populate_info()
        self.populate_usage()

    def populate_usage(self):
        """
        Populates the usage tab with a line chart for usage percent and a ScrollableInfoFrame for pe core usage.
        :return: void
        """
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
        """
        Populates the info tab with a ScrollableInfoFrame that displays the CPU info.
        :return:
        """
        cpu_info = get_cpu_info()
        self.info_frame = ScrollableInfoFrame(master=self.tabview.tab("info"),
                                              command=None,
                                              item_list=cpu_info.items(), width=self.width - 20,
                                              height=self.height - 20)
        self.info_frame.grid(row=0, column=0, padx=15, pady=15, sticky="ns")

    def init_per_core_usage(self, parent):
        """
        Initializes the per core usage ScrollableInfoFrame.
        :param parent:
        :return:
        """
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
        """
        Updates the per core usage ScrollableInfoFrame.
        :return:
        """
        cpus = get_per_core_usage()
        self.per_core_usage.update_items(cpus.items())
        self.per_core_usage.after(1000, self.update_per_core_usage)

    def save_as_csv(self):
        """
        Saves the state of the CPU tab as csv. state = the current state of the line chart and the ScrollableInfoFrame.
        :return:
        """
        self.chart.save_state_as_csv(f'{self.export_path}/usage.csv')
        self.per_core_usage.save_state_as_csv(f'{self.export_path}/per_core.csv')
