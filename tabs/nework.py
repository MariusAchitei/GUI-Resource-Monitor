import customtkinter
import mplcyberpunk
import psutil
from matplotlib import pyplot as plt
import time

from tabs.common.line_chart import LineChart
from tabs.threads.networkMonitor import NetworkMonitorThread
from utils.general_utils import speed_bytes2human2

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
