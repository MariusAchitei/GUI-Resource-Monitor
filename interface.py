import customtkinter
import os
from PIL import Image
from tabs.main import TABS


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("GUI-Resource-Monitor")
        self.geometry("800x550")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(26, 26))

        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")),
                                                 size=(20, 20))

        self.add_user_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        # self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Resource-Monitor",
                                                             image=self.logo_image,
                                                             compound="left",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        for index, tab in enumerate(TABS):
            TABS[tab]["button"] = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                          border_spacing=10, text=tab.capitalize(),
                                                          fg_color="transparent", text_color=("gray10", "gray90"),
                                                          hover_color=("gray70", "gray30"),
                                                          image=self.home_image, anchor="w",
                                                          command=self.tab_button_event(tab))
            TABS[tab]["button"].grid(row=index + 1, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame,
                                                                values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=len(TABS) + 3, column=0, padx=20, pady=20, sticky="s")

        # create frames for all pages

        for tab in TABS:
            TABS[tab]["frame"] = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name(list(TABS.keys())[0])

        for tab in TABS:
            TABS[tab]["init"](TABS[tab]["frame"])

    def tab_button_event(self, name):
        return lambda: self.select_frame_by_name(name)

    def select_frame_by_name(self, name):
        # set button color for selected button
        for tab in TABS:
            TABS[tab]["button"].configure(fg_color=("gray75", "gray25") if name == tab else "transparent")
            # show selected frame
            if name == tab:
                TABS[tab]["frame"].grid(row=0, column=1, sticky="nsew")
            else:
                TABS[tab]["frame"].grid_forget()

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()
