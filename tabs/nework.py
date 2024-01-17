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
        """
        Initializes the Network tab. It creates 3 tabs: speeds, devices and connections.
        :param root: the root of the tab.
        """
        super().__init__(root)
        self.screenshot_path = f'{self.screenshot_path}/network'
        self.export_path = f'{self.export_path}/network'
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
        """
        Initializes the speeds tab. It creates 2 tabs: download and upload as line charts each running on a separate thread.
        beacause the update function is blocking.
        :param tab: the tab that will be populated.
        :return: void
        """
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
        """
        Initializes the devices tab. It creates a tab for each device.
        :param tab: the tab that will be populated.
        :return: void
        """
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
        """
        Initializes the connections tab. It creates a ScrollableInfoFrame that displays the connections info.
        :param tab: the tab that will be populated.
        :return: void
        """
        connections_info = get_connections_network_info()
        frame = ScrollableInfoFrame(master=tab, item_list=connections_info.items(), command=None, width=self.width - 20,
                                    height=self.height - 20)
        frame.grid(row=0, column=0, padx=15, pady=15, sticky="ns")

    def populate_device_tabs(self, device_tabs):
        """
        Populates the device tabs with a ScrollableInfoFrame that displays the device info.
        :param device_tabs: for every device, a tuple containing the tab and the device info.
        :return: void
        """
        frames = []
        for (tab, info) in device_tabs:
            frame = ScrollableInfoFrame(master=tab, item_list=info.items(), command=None, width=self.width - 20,
                                        height=self.height - 20)
            frame.grid(row=0, column=0, padx=15, pady=15, sticky="ns")
            pass

    def save_as_csv(self):
        """
        Saves the download and upload speeds as csv.
        :return: void
        """
        self.download_chart.save_state_as_csv(f'{self.export_path}/speeds/download.csv')
        self.upload_chart.save_state_as_csv(f'{self.export_path}/speeds/upload.csv')
