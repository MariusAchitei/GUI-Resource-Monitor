import os
import shutil

import customtkinter
import matplotlib.pyplot as plt
import psutil

from tabs.common.ScrollableInfoFrame import ScrollableInfoFrame
from tabs.common.pie_chart import PieChart

from utils.general_utils import bytes2human

WIDTH = 500
HEIGHT = 400


def init_disk(root):
    plt.style.use("cyberpunk")
    DiskTab(root)


def get_partitions():
    return [part for part in psutil.disk_partitions(all=False) if
            not (os.name == 'nt' and ('cdrom' in part.opts or part.fstype == ''))]


def populate_partition(tab, part):
    usage = shutil.disk_usage(part.mountpoint)
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
    usage = shutil.disk_usage(part.mountpoint)
    info = {
        "Device": part.device,
        "Total": bytes2human(usage.total),
        "Used": bytes2human(usage.used),
        "Free": bytes2human(usage.free),
        "Use": f'{usage.used * 100 // usage.total}%',
        "Type": part.fstype,
        "Mount": part.mountpoint
    }
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
        self.populate_()

    def populate_(self):
        for i, part in enumerate(self.partitions):
            populate_partition(self.tabview.tab(part.mountpoint), part)
