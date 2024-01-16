import os
import pickle

import customtkinter
from PIL import ImageGrab

from utils.general_utils import create_directory_if_not_exists, get_current_date_time

screenshot_path = "./screenshots"
export_path = "./exports"
state_path = "./states"
WIDTH = 650
HEIGHT = 700


class BaseTab:
    def __init__(self, root, width=WIDTH, height=HEIGHT):
        self.root = root
        self.screenshot_path = f'{screenshot_path}/other'
        self.export_path = f'{export_path}'
        self.state_path = f'{state_path}'
        self.width = width
        self.height = height

        self.top_frame = customtkinter.CTkFrame(root)
        self.top_frame.grid(row=0, column=0, sticky="nsew")

        self.save_fig_button = customtkinter.CTkButton(master=self.top_frame, text="📷", command=self.save_tab)
        self.save_fig_button.grid(row=0, column=0, padx=20, pady=20, sticky="n")

        self.export_button = customtkinter.CTkButton(master=self.top_frame, text="export", command=self.save_as_csv)
        self.export_button.grid(row=0, column=1, padx=20, pady=20, sticky="n")

        self.export_button = customtkinter.CTkButton(master=self.top_frame, text="save state", command=self.save_state)
        self.export_button.grid(row=0, column=2, padx=20, pady=20, sticky="n")

        self.tabview = customtkinter.CTkTabview(root, width=self.width, height=self.height)
        self.tabview.grid(row=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

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

    def save_state(self):
        path = f'{self.state_path}/state{get_current_date_time()}.pkl'
        os.makedirs(os.path.dirname(path), exist_ok=True)
        state = self.get_state()
        with open(path, "wb") as file:
            pickle.dump(state, file)

    def get_state(self):
        return self

    def load_state(self, file_path):
        # file_path = "D:\.facultate\pyton\GUI-Resource-Monitor\states\cpu\state2021-05-16 17-05-01.pkl"
        try:
            with open(file_path, "rb") as file:
                state = pickle.load(file)
                return state
        except FileNotFoundError:
            print("File not found.")
        except Exception as e:
            print(f"Error loading state: {str(e)}")

    def set_state(self, state):
        pass
