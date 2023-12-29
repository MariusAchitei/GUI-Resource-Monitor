import customtkinter

from tabs.common.ScrollableInfoFrame import ScrollableInfoFrame
from tabs.common.line_chart import LineChart
import matplotlib.pyplot as plt
import mplcyberpunk
import psutil

import cpuinfo

WIDTH = 500
HEIGHT = 400


def init_cpu(root):
    plt.style.use("cyberpunk")
    CpuTab(root)


def update_cpu_function():
    return psutil.cpu_percent()


class CpuTab:
    def __init__(self, root):
        self.tabview = customtkinter.CTkTabview(root, width=WIDTH, height=HEIGHT)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("info")
        self.tabview.add("usage")
        self.tabview.tab("info").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("usage").grid_columnconfigure(0, weight=1)
        self.populate_info()
        LineChart(self.tabview.tab("usage"), update_cpu_function, mplcyberpunk.add_glow_effects)

    def populate_info(self):
        info = cpuinfo.get_cpu_info()
        cpu_info = {
            "Brand": info["brand_raw"],
            "Architecture": info["arch"],
            "Bits": info["bits"],
            "Cores": psutil.cpu_count(logical=False),
            "Threads": psutil.cpu_count(logical=True),
            "Frequency": info["hz_actual_friendly"],
            "L2 Cache": info["l2_cache_size"],
            "L3 Cache": info["l3_cache_size"],
            "Vendor": info["vendor_id_raw"],
            # "Family": info["family_raw"],
            # "Model": info["model_raw"],
            "Stepping": info["stepping"],
            "Flags": info["flags"]
        }
        self.info_frame = ScrollableInfoFrame(master=self.tabview.tab("info"),
                                              command=None,
                                              item_list=cpu_info.items(), width=WIDTH - 20,
                                              height=HEIGHT - 20)
        self.info_frame.grid(row=0, column=0, padx=15, pady=15, sticky="ns")
