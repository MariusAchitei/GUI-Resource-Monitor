import customtkinter

from tabs.common.ScrollableInfoFrame import ScrollableInfoFrame
from tabs.common.base_tab import BaseTab
from tabs.common.line_chart import LineChart
import matplotlib.pyplot as plt
import mplcyberpunk
from utils.memory_utils import *
from utils.general_utils import bytes2human


def init_memory(root):
    plt.style.use("cyberpunk")
    MemoryTab(root)


def y_label_function(x):
    if type(x) == int:
        return bytes2human(int(x))
    return bytes2human(int(float(x)))


class MemoryTab(BaseTab):
    def __init__(self, root):
        super().__init__(root)
        self.screenshot_path = f'{self.screenshot_path}/memory'
        self.export_path = f'{self.export_path}/memory'
        self.state_path = f'{self.state_path}/memory'
        self.tabview.add("info")
        self.tabview.add("usage")
        self.tabview.tab("info").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("usage").grid_columnconfigure(0, weight=1)
        self.populate_info()
        self.populate_usage()
        # LineChart(self.tabview.tab("usage"), memory_update_function, mplcyberpunk.add_glow_effects)

    def populate_info(self):
        self.infotabview = customtkinter.CTkTabview(self.tabview.tab("info"), width=self.width - 20,
                                                    height=self.height - 20)
        self.infotabview.grid(row=0, column=2, sticky="nsew")
        self.info_tabs = []
        for index, info in enumerate(get_ram_info()):
            self.infotabview.add(f"Slot {index + 1}")
            self.infotabview.tab(f"Slot {index + 1}").grid_columnconfigure(0, weight=1)
            info_tab = ScrollableInfoFrame(master=self.infotabview.tab(f"Slot {index + 1}"),
                                           command=None,
                                           item_list=info.items(), width=self.width - 20,
                                           height=self.height - 20)
            info_tab.grid(row=0, column=0, padx=15, pady=15, sticky="ns")
            self.info_tabs.append(info_tab)

    def populate_usage(self):
        self.usagetabview = customtkinter.CTkTabview(self.tabview.tab("usage"), width=self.width, height=self.height)
        self.usagetabview.grid(row=0, column=2, sticky="nsew")
        self.usagetabview.add("precent")
        self.usagetabview.add("bytes")
        self.usagetabview.tab("precent").grid_columnconfigure(0, weight=1)
        self.usagetabview.tab("bytes").grid_columnconfigure(0, weight=1)
        self.usage_tabs = []
        self.precent_usage_tab = LineChart(self.usagetabview.tab("precent"), memory_precent_update_function,
                                           mplcyberpunk.add_glow_effects,
                                           screenshot_path=f'{self.screenshot_path}/usage/precent',
                                           title="Memory Usage in Precent")
        self.bytes_usage_tab = LineChart(self.usagetabview.tab("bytes"), memory_bytes_update_function,
                                         mplcyberpunk.add_glow_effects,
                                         y_limit=get_memory_limit(),
                                         y_label_function=y_label_function,
                                         screenshot_path=f'{self.screenshot_path}/usage/bytes',
                                         title="Memory Usage in Bytes")

    def save_as_csv(self):
        self.precent_usage_tab.save_state_as_csv(f'{self.export_path}/usage/precent.csv')
        self.bytes_usage_tab.save_state_as_csv(f'{self.export_path}/usage/bytes.csv')

    def get_state(self):
        return {
            "info_tabs": self.info_tabs,
            "usage_tabs": self.usage_tabs,

        }

    def load_state(self, state):
        self.info_tabs = state["info_tabs"]
        self.usage_tabs = state["usage_tabs"]
        for info_tab in self.info_tabs:
            self.populate_info(info_tab)
        for usage_tab in self.usage_tabs:
            self.populate_usage(usage_tab)
