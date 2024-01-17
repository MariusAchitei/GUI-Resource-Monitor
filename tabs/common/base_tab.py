import customtkinter
from PIL import ImageGrab

from utils.general_utils import create_directory_if_not_exists, get_current_date_time

screenshot_path = "./screenshots"
export_path = "./exports"
WIDTH = 650
HEIGHT = 700


class BaseTab:
    """
    Base class for all tabs that are used in the application.
    """

    def __init__(self, root, width=WIDTH, height=HEIGHT):
        """
        Initializes the tab adding to it a tabView, the screenshot and export button.
        Sets default width and height for the tab.
        Sets default screenshot and export path for the tab.
        :param root: the root of the tab
        :param width: the width of the tab
        :param height: the height of the tab
        """
        self.root = root
        self.screenshot_path = f'{screenshot_path}/other'
        self.export_path = f'{export_path}'
        self.width = width
        self.height = height

        self.top_frame = customtkinter.CTkFrame(root)
        self.top_frame.grid(row=0, column=0, sticky="nsew")
        self.save_fig_button = customtkinter.CTkButton(master=self.top_frame, text="📷", command=self.save_tab)
        self.save_fig_button.grid(row=0, column=0, padx=20, pady=20, sticky="n")

        self.export_button = customtkinter.CTkButton(master=self.top_frame, text="export", command=self.save_as_csv)
        self.export_button.grid(row=0, column=1, padx=20, pady=20, sticky="n")

        self.tabview = customtkinter.CTkTabview(root, width=self.width, height=self.height)
        self.tabview.grid(row=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

    def save_tab(self):
        """
        Saves the tab as a screenshot.
        :return: void
        """
        x = self.root.winfo_rootx()
        y = self.root.winfo_rooty()
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))

        create_directory_if_not_exists(self.screenshot_path)

        screenshot.save(f'{self.screenshot_path}/screen-shot{get_current_date_time()}.png')

    def save_as_csv(self):
        """
        It is a virtual method that should be implemented in the child classes in order to export the data from the panel to a csv file.
        :return: void
        """
        pass
