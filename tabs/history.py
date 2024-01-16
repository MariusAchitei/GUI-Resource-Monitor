import os

from tabs.common.ScrollableInfoFrame import ScrollableInfoFrame
from tabs.common.base_tab import BaseTab
from tabs.common.line_chart import LineChart
import matplotlib.pyplot as plt
import mplcyberpunk

from utils.cpu_utils import *


def init_history(root):
    plt.style.use("cyberpunk")
    HistoryTab(root)


class HistoryTab(BaseTab):
    def __init__(self, root):
        super().__init__(root)
        self.tabview.add("usage")
        path = './states/cpu/state2024-01-16-07-06-45.pkl'
        if not os.path.exists(path):
            return
        state = super().load_state(path)
        chart = LineChart(self.tabview.tab("usage"), lambda x: None,
                          effects=mplcyberpunk.add_glow_effects,
                          screenshot_path=f'{self.screenshot_path}/usage',
                          title="CPU Usage", state=state)
        # chart.load_state(content)
