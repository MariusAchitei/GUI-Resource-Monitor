import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class PieChart:
    def __init__(self, root, proportions, labels, title):
        wedge_colors = ['#86c7f3', '#8be06e', '#f39c7c', '#ffb366']
        background_color = '#302c2c'

        self.root = root
        self.proportions = proportions
        self.labels = labels
        self.title = title
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        wedges, texts, autotexts = self.ax.pie(proportions, labels=labels, autopct='%1.1f%%', startangle=90,
                                               colors=wedge_colors, wedgeprops=dict(width=0.3))

        self.fig.patch.set_facecolor(background_color)

        for text, autotext in zip(texts, autotexts):
            text.set_color('white')
            autotext.set_color('white')

        self.ax.axis('equal')
        self.ax.set_title(title)
        self.canvas.get_tk_widget().pack()
