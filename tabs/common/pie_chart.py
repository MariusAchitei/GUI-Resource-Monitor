import customtkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from tabs.common.base_chart import BaseChart


class PieChart(BaseChart):
    """
    Class used to create a very customisable pie chart.
    """

    def __init__(self, root, proportions, labels, title="Pie Chart", screenshot_path='screenshots/other'):
        """
        Initializes the pie chart.
        :param root: the root of the pie chart.
        :param proportions: the proportions of the pie chart.
        :param labels: the labels of the pie chart.
        :param title: the title of the pie chart.
        :param screenshot_path: the path where the screenshots of the pie chart will be saved.
        """
        super().__init__(root, screenshot_path=screenshot_path)

        wedge_colors = ['#86c7f3', '#8be06e', '#f39c7c', '#ffb366']
        background_color = '#302c2c'

        self.proportions = proportions
        self.labels = labels
        self.title = title
        wedges, texts, autotexts = self.ax.pie(proportions, labels=labels, autopct='%1.1f%%', startangle=90,
                                               colors=wedge_colors, wedgeprops=dict(width=0.3))

        self.fig.patch.set_facecolor(background_color)

        for text, autotext in zip(texts, autotexts):
            text.set_color('white')
            autotext.set_color('white')

        self.ax.axis('equal')
        self.ax.set_title(title)
