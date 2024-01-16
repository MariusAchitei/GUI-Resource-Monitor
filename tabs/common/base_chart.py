from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import customtkinter
from utils.general_utils import get_current_date_time, create_directory_if_not_exists


class BaseChart:
    def __init__(self, root, screenshot_path='screenshots/other'):
        self.screenshot_path = screenshot_path
        self.root = root
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()
        self.save_fig_button = customtkinter.CTkButton(master=root, text="Save Figure", command=self.save_chart)
        self.save_fig_button.pack(padx=20, pady=10)

    def save_chart(self):
        create_directory_if_not_exists(self.screenshot_path)
        self.fig.savefig(f'{self.screenshot_path}/{get_current_date_time()}.png')
