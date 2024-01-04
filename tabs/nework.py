import subprocess
import re

import customtkinter
import mplcyberpunk
import psutil
from matplotlib import pyplot as plt
import time

from tabs.common.ScrollableInfoFrame import ScrollableInfoFrame
from tabs.common.line_chart import LineChart
from tabs.threads.networkMonitor import NetworkMonitorThread
from utils.general_utils import speed_bytes2human2
from utils.network_utils import get_connections_network_info

WIDTH = 500
HEIGHT = 400


def init_network(root):
    plt.style.use("cyberpunk")
    NetworkTab(root)


def update_download_speed():
    initial_data = psutil.net_io_counters()
    interval = 1
    time.sleep(interval)
    final_data = psutil.net_io_counters()

    return (final_data.bytes_recv - initial_data.bytes_recv) / interval


def update_upload_speed():
    initial_data = psutil.net_io_counters()
    interval = 1
    time.sleep(interval)
    final_data = psutil.net_io_counters()

    return (final_data.bytes_sent - initial_data.bytes_sent) / interval


class NetworkTab:
    def __init__(self, root):
        self.tabview = customtkinter.CTkTabview(root, width=WIDTH, height=HEIGHT)
        self.tabview.grid(row=0, column=0, sticky="nsew")
        self.tabview.add("speeds")
        self.tabview.add("devices")
        self.tabview.add("connections")
        self.tabview.tab("speeds").grid_columnconfigure(0, weight=1)
        self.tabview.tab("devices").grid_columnconfigure(0, weight=1)
        self.tabview.tab("connections").grid_columnconfigure(0, weight=1)
        self.init_speeds_tab(self.tabview.tab("speeds"))
        self.init_devices_tab(self.tabview.tab("devices"))
        self.init_connections_tab(self.tabview.tab("connections"))

    def init_speeds_tab(self, tab):
        self.speeds_tab_view = customtkinter.CTkTabview(tab, width=WIDTH - 20, height=HEIGHT - 20)
        self.speeds_tab_view.grid(row=0, column=0, sticky="nsew")
        self.speeds_tab_view.add("download")
        self.speeds_tab_view.add("upload")
        self.speeds_tab_view.tab("download").grid_columnconfigure(0, weight=1)
        self.speeds_tab_view.tab("upload").grid_columnconfigure(0, weight=1)

        self.download_chart = LineChart(self.speeds_tab_view.tab("download"), update_download_speed,
                                        y_label_function=speed_bytes2human2,
                                        dinamic_y_limit=True, effects=mplcyberpunk.add_glow_effects, self_update=False)
        self.upload_chart = LineChart(self.speeds_tab_view.tab("upload"), update_upload_speed,
                                      y_label_function=speed_bytes2human2,
                                      dinamic_y_limit=True, effects=mplcyberpunk.add_glow_effects, self_update=False)
        NetworkMonitorThread(1, self.download_chart.update_line_chart).start()
        NetworkMonitorThread(1, self.upload_chart.update_line_chart).start()

    def init_devices_tab(self, tab):
        for key, value in psutil.net_if_stats().items():
            print(f'{key}: {value}')
        print(psutil.net_if_stats())
        self.devices_tab_view = customtkinter.CTkTabview(tab, width=WIDTH - 20, height=HEIGHT - 20)
        device_tabs_info = []
        for key, value in psutil.net_if_stats().items():
            if not value.isup:
                continue
            self.devices_tab_view.add(key)
            self.devices_tab_view.tab(key).grid_columnconfigure(0, weight=1)
            device_tabs_info.append((self.devices_tab_view.tab(key), value))
        self.devices_tab_view.grid(row=0, column=0)
        populate_device_tabs(device_tabs_info)

    def init_connections_tab(self, tab):
        connections_info = get_connections_network_info()
        frame = ScrollableInfoFrame(master=tab, item_list=connections_info.items(), command=None, width=WIDTH - 20,
                                    height=HEIGHT - 20)
        frame.grid(row=0, column=0, padx=15, pady=15, sticky="ns")


def populate_device_tabs(device_tabs):
    frames = []
    for (tab, info) in device_tabs:
        frame = ScrollableInfoFrame(master=tab, item_list=info._asdict().items(), command=None, width=WIDTH - 20,
                                    height=HEIGHT - 20)
        frame.grid(row=0, column=0, padx=15, pady=15, sticky="ns")
        pass
