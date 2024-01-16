import customtkinter
import matplotlib.pyplot as plt
from tabs.common.ScrollableInfoFrame import ScrollableInfoFrame
from tabs.common.base_tab import BaseTab
from tabs.common.pie_chart import PieChart

from utils.disk_utils import *


def init_disk(root):
    plt.style.use("cyberpunk")
    DiskTab(root)


class DiskTab(BaseTab):

    def __init__(self, root):
        super().__init__(root)
        self.screenshot_path = f'{self.screenshot_path}/disk'
        self.export_path = f'{self.export_path}/disk'
        self.info_tabs = []
        self.partitions = []
        for part in get_partitions():
            self.tabview.add(part.mountpoint)
            self.partitions.append(part)
            self.tabview.tab(part.mountpoint).grid_columnconfigure(0, weight=1)
            self.populate_partition(self.tabview.tab(part.mountpoint), part)

    def populate_partition(self, tab, part):
        usage = get_partition_usage(part)
        tabview = customtkinter.CTkTabview(tab, width=self.width - 20, height=self.height - 20)
        tabview.grid(row=0, column=2, sticky="nsew")
        tabview.add("info")
        tabview.add("chart")
        tabview.tab("info").grid_columnconfigure(0, weight=1)
        tabview.tab("chart").grid_columnconfigure(0, weight=1)
        PieChart(tabview.tab("chart"), [usage.used * 100 // usage.total, 100 - usage.used * 100 // usage.total],
                 ["Used", "Free"], title=f'{part.mountpoint} memory usage',
                 screenshot_path=f'{self.screenshot_path}/{part.mountpoint}')
        self.populate_info(tabview.tab("info"), part)

    def populate_info(self, tab, part):
        info = get_partition_info(part)

        info_frame = ScrollableInfoFrame(master=tab,
                                         item_list=info.items(),
                                         width=self.width - 20,
                                         height=self.height - 20)
        info_frame.grid(row=0, column=0, padx=15, pady=15, sticky="ns")
        self.info_tabs.append(info_frame)

    def save_as_csv(self):
        for info_tab in self.info_tabs:
            info_tab.save_as_csv()
