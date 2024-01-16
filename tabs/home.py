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
    print(os.path.exists(file_name))
    try:
        print(file_name)
        subprocess.run(['notepad.exe', file_name])
    except Exception as e:
        print(e)


class Home(BaseTab):
    def __init__(self, root):
        super().__init__(root)
        self.screenshot_path = f'{self.screenshot_path}/home'
        self.export_path = f'{self.export_path}/home'
        self.tabview.add("info")

        for index, file in enumerate(list_csv_files(export_path)):
            self.save_fig_button = customtkinter.CTkButton(master=self.tabview.tab("info"),
                                                           text="📝 " + file.split("/")[-1],
                                                           command=lambda: on_file_select(file))
            self.save_fig_button.pack(padx=20, pady=10)

    def populate_info(self):
        pass
