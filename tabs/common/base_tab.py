import customtkinter
from PIL import ImageGrab

from utils.general_utils import create_directory_if_not_exists, get_current_date_time

screenshot_path = "./screenshots"
export_path = "./exports"
WIDTH = 800
HEIGHT = 700


class BaseTab:
    def __init__(self, root, width=WIDTH, height=HEIGHT):
        self.root = root
        self.screenshot_path = f'{screenshot_path}/other'
        self.export_path = f'{export_path}'
        self.width = width
        self.height = height

        self.save_fig_button = customtkinter.CTkButton(master=root, text="📷", command=self.save_tab)
        self.save_fig_button.grid(row=0, column=0, padx=20, pady=20, sticky="n")

        self.export_button = customtkinter.CTkButton(master=root, text="export", command=self.save_as_csv)
        self.export_button.grid(row=0, column=2, padx=20, pady=20, sticky="n")

        self.tabview = customtkinter.CTkTabview(root, width=self.width, height=self.height)
        self.tabview.grid(row=1, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")

    def save_tab(self):
        x = self.root.winfo_rootx()
        y = self.root.winfo_rooty()
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))

        create_directory_if_not_exists(self.screenshot_path)

        screenshot.save(f'{self.screenshot_path}/screen-shot{get_current_date_time()}.png')

    def save_as_csv(self):
        pass
