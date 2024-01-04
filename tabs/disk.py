import shutil

import customtkinter
import matplotlib.pyplot as plt
from tabs.common.ScrollableInfoFrame import ScrollableInfoFrame
from tabs.common.pie_chart import PieChart

from utils.disk_utils import *
from utils.general_utils import bytes2human

WIDTH = 500
HEIGHT = 400


def init_disk(root):
    plt.style.use("cyberpunk")
    DiskTab(root)


def populate_partition(tab, part):
    usage = get_partition_usage(part)
    tabview = customtkinter.CTkTabview(tab, width=WIDTH - 20, height=HEIGHT - 20)
    tabview.grid(row=0, column=2, sticky="nsew")
    tabview.add("info")
    tabview.add("chart")
    tabview.tab("info").grid_columnconfigure(0, weight=1)
    tabview.tab("chart").grid_columnconfigure(0, weight=1)
    PieChart(tabview.tab("chart"), [usage.used * 100 // usage.total, 100 - usage.used * 100 // usage.total],
             ["Used", "Free"], "Usage")
    populate_info(tabview.tab("info"), part)


def populate_info(tab, part):
    info = get_partition_info(part)
    info_frame = ScrollableInfoFrame(master=tab,
                                     item_list=info.items(),
                                     width=WIDTH - 20,
                                     height=HEIGHT - 20)
    info_frame.grid(row=0, column=0, padx=15, pady=15, sticky="ns")


class DiskTab:

    def __init__(self, root):
        self.tabview = customtkinter.CTkTabview(root, width=WIDTH, height=HEIGHT)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.partitions = []
        for part in get_partitions():
            self.tabview.add(part.mountpoint)
            self.partitions.append(part)
            self.tabview.tab(part.mountpoint).grid_columnconfigure(0, weight=1)
            populate_partition(self.tabview.tab(part.mountpoint), part)
