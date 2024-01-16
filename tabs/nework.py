import customtkinter
import mplcyberpunk
from matplotlib import pyplot as plt

from tabs.common.base_tab import BaseTab
from utils.network_utils import *

from tabs.common.ScrollableInfoFrame import ScrollableInfoFrame
from tabs.common.line_chart import LineChart
from tabs.threads.networkMonitor import NetworkMonitorThread
from utils.general_utils import speed_bytes2human2


def init_network(root):
    plt.style.use("cyberpunk")
    NetworkTab(root)


class NetworkTab(BaseTab):
    def __init__(self, root):
        super().__init__(root)
        self.screenshot_path = f'{self.screenshot_path}/network'
        self.export_path = f'{self.export_path}/network'
        self.state_path = f'{self.state_path}/network'
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
        self.speeds_tab_view = customtkinter.CTkTabview(tab, width=self.width - 20, height=self.height - 20)
        self.speeds_tab_view.grid(row=0, column=0, sticky="nsew")
        self.speeds_tab_view.add("download")
        self.speeds_tab_view.add("upload")
        self.speeds_tab_view.tab("download").grid_columnconfigure(0, weight=1)
        self.speeds_tab_view.tab("upload").grid_columnconfigure(0, weight=1)

        self.download_chart = LineChart(self.speeds_tab_view.tab("download"), update_download_speed,
                                        y_label_function=speed_bytes2human2,
                                        dinamic_y_limit=True, effects=mplcyberpunk.add_glow_effects, self_update=False,
                                        title="Download Speed",
                                        screenshot_path=f'{self.screenshot_path}/download')
        self.upload_chart = LineChart(self.speeds_tab_view.tab("upload"), update_upload_speed,
                                      y_label_function=speed_bytes2human2,
                                      dinamic_y_limit=True, effects=mplcyberpunk.add_glow_effects, self_update=False,
                                      title="Upload Speed",
                                      screenshot_path=f'{self.screenshot_path}/upload')
        NetworkMonitorThread(1, self.download_chart.update_line_chart).start()
        NetworkMonitorThread(1, self.upload_chart.update_line_chart).start()

    def init_devices_tab(self, tab):
        self.devices_tab_view = customtkinter.CTkTabview(tab, width=self.width - 20, height=self.height - 20)
        device_tabs_info = []
        info = get_devices_info()
        for key, value in info.items():
            self.devices_tab_view.add(key)
            self.devices_tab_view.tab(key).grid_columnconfigure(0, weight=1)
            device_tabs_info.append((self.devices_tab_view.tab(key), value))
        self.devices_tab_view.grid(row=0, column=0)
        self.populate_device_tabs(device_tabs_info)

    def init_connections_tab(self, tab):
        connections_info = get_connections_network_info()
        frame = ScrollableInfoFrame(master=tab, item_list=connections_info.items(), command=None, width=self.width - 20,
                                    height=self.height - 20)
        frame.grid(row=0, column=0, padx=15, pady=15, sticky="ns")

    def populate_device_tabs(self, device_tabs):
        frames = []
        for (tab, info) in device_tabs:
            frame = ScrollableInfoFrame(master=tab, item_list=info.items(), command=None, width=self.width - 20,
                                        height=self.height - 20)
            frame.grid(row=0, column=0, padx=15, pady=15, sticky="ns")
            pass

    def save_as_csv(self):
        self.download_chart.save_state_as_csv(f'{self.export_path}/speeds/download.csv')
        self.upload_chart.save_state_as_csv(f'{self.export_path}/speeds/upload.csv')

    def get_state(self):
        return {
            "download_chart": self.download_chart.get_state(),
            "upload_chart": self.upload_chart.get_state(),
        }

    def load_state(self, state):
        self.download_chart.load_state(state["download_chart"])
        self.upload_chart.load_state(state["upload_chart"])
