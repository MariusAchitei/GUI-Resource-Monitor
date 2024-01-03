import subprocess

import customtkinter

from tabs.common.ScrollableInfoFrame import ScrollableInfoFrame
from tabs.common.line_chart import LineChart
import matplotlib.pyplot as plt
import psutil
import mplcyberpunk
from utils.memory_utils import get_memory_type_by_code
from utils.general_utils import bytes2human

WIDTH = 500
HEIGHT = 400


def init_memory(root):
    plt.style.use("cyberpunk")
    MemoryTab(root)


def memory_precent_update_function():
    return psutil.virtual_memory().percent


def memory_bytes_update_function():
    return psutil.virtual_memory().used


def get_memory_limit():
    return 0, psutil.virtual_memory().total


def y_label_function(x):
    if type(x) == int:
        return bytes2human(int(x))
    return bytes2human(int(float(x)))


# 0740688443
# 0765063494
def get_ram_info():
    cmd = "wmic MemoryChip get /format:csv"
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    result, error = process.communicate()
    print(result)
    data = []
    lines = [line for line in result.split("\n") if line != ""]
    key_line = lines[0]
    keys = [key for key in key_line.split(",")]
    value_lines = [line for (index, line) in enumerate(lines) if index > 0 and line != ""]
    for index, line in enumerate(value_lines):
        slot = {}
        values = [value for value in line.split(",")]
        for i in range(0, len(values)):
            slot[keys[i]] = values[i]
        slot["Capacity"] = bytes2human(int(slot["Capacity"]))
        slot["ConfiguredClockSpeed"] = f"{slot['ConfiguredClockSpeed']} MHz"
        slot["Speed"] = f"{slot['Speed']} MHz"
        slot["MemoryType"] = get_memory_type_by_code(slot["MemoryType"])
        data.append(slot)
    if error:
        return error
    return data


class MemoryTab:
    def __init__(self, root):
        self.tabview = customtkinter.CTkTabview(root, width=WIDTH, height=HEIGHT)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("info")
        self.tabview.add("usage")
        self.tabview.tab("info").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("usage").grid_columnconfigure(0, weight=1)
        self.populate_info()
        self.populate_usage()
        # LineChart(self.tabview.tab("usage"), memory_update_function, mplcyberpunk.add_glow_effects)

    def populate_info(self):
        self.infotabview = customtkinter.CTkTabview(self.tabview.tab("info"), width=WIDTH - 20, height=HEIGHT - 20)
        self.infotabview.grid(row=0, column=2, sticky="nsew")
        self.info_tabs = []
        for index, info in enumerate(get_ram_info()):
            self.infotabview.add(f"Slot {index + 1}")
            self.infotabview.tab(f"Slot {index + 1}").grid_columnconfigure(0, weight=1)
            info_tab = ScrollableInfoFrame(master=self.infotabview.tab(f"Slot {index + 1}"),
                                           command=None,
                                           item_list=info.items(), width=WIDTH - 20,
                                           height=HEIGHT - 20)
            info_tab.grid(row=0, column=0, padx=15, pady=15, sticky="ns")
            self.info_tabs.append(info_tab)

    def populate_usage(self):
        self.usagetabview = customtkinter.CTkTabview(self.tabview.tab("usage"), width=WIDTH, height=HEIGHT)
        self.usagetabview.grid(row=0, column=2, sticky="nsew")
        self.usagetabview.add("precent")
        self.usagetabview.add("bytes")
        self.usagetabview.tab("precent").grid_columnconfigure(0, weight=1)
        self.usagetabview.tab("bytes").grid_columnconfigure(0, weight=1)
        self.usage_tabs = []
        precent_usage_tab = LineChart(self.usagetabview.tab("precent"), memory_precent_update_function,
                                      mplcyberpunk.add_glow_effects)
        bytes_usage_tab = LineChart(self.usagetabview.tab("bytes"), memory_bytes_update_function,
                                    mplcyberpunk.add_glow_effects,
                                    y_limit=get_memory_limit(),
                                    y_label_function=y_label_function)
