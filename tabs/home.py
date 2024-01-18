from tabs.common.base_tab import BaseTab
import os
import glob
import subprocess
import customtkinter

export_path = "./exports"


def init_home(root):
    Home(root)
    pass


def list_csv_files(folder_path):
    """ Lists all CSV files in the given folder. """
    csv_files = []
    for root, dirs, files in os.walk(export_path):
        for file in files:
            if file.endswith('.csv'):
                csv_files.append(os.path.join(root, file))
    return csv_files


def on_file_select(file_name):
    """ Opens the given file in notepad."""
    print(os.path.exists(file_name))
    try:
        print(file_name)
        subprocess.run(['notepad.exe', file_name])
    except Exception as e:
        print(e)


def select_file(file_path):
    """ Opens a file selection dialog. """
    return lambda: on_file_select(file_path)


class Home(BaseTab):
    """
    Class used to create the Home tab. It inherits from BaseTab. It has 1 tab, the selectable csv panel.
    """

    def __init__(self, root):
        """
        Initializes the Home tab. It creates the selectable csv panel.
        :param root: the root of the tab.
        """
        super().__init__(root)
        self.screenshot_path = f'{self.screenshot_path}/home'
        self.export_path = f'{self.export_path}/home'
        self.tabview.add("info")

        for index, file in enumerate(list_csv_files(export_path)):
            self.save_fig_button = customtkinter.CTkButton(master=self.tabview.tab("info"),
                                                           text="📝 " + file.split("/")[-1],
                                                           command=select_file(file))
            self.save_fig_button.pack(padx=20, pady=10)

    def populate_info(self):
        pass
