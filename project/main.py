import tkinter
import customtkinter

# System appearance settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        """
        Window configuration
        """
        self.title("Cyber Security Simulator")
        self.geometry(f"{1100}x{580}")

        """
        -------------------------------------------------------------------------------------------
        Window layout
        """
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        """
        -------------------------------------------------------------------------------------------
        Sidebar
        """
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Simulator settings", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        """
        -------------------------------------------------------------------------------------------
        Main frame
        """
        self.tabview = customtkinter.CTkTabview(self, width=880, height=550)
        self.tabview.grid(row=0, column=1, columnspan=4, rowspan=4, padx=(10, 0), sticky="nesw")
        self.tabview.add("System")
        self.tabview.add("Attacker")
        self.tabview.add("Defender")

        """
        -------------------------------------------------------------------------------------------
        Configure grid of individual tabs
        """
        self.tabview.tab("System").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Attacker").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Defender").grid_columnconfigure(0, weight=1)


        """
        -------------------------------------------------------------------------------------------
        System tab
        """
        self.label_system = customtkinter.CTkLabel(self.tabview.tab("System"), text="This is the system tab")
        self.label_system.grid(row=0, column=0, padx=20, pady=20)

        """
        -------------------------------------------------------------------------------------------
        Attacker tab
        """
        self.label_attacker = customtkinter.CTkLabel(self.tabview.tab("Attacker"), text="This is the attacker tab")
        self.label_attacker.grid(row=0, column=0, padx=20, pady=20)

        """
        -------------------------------------------------------------------------------------------
        Defender tab
        """
        self.label_defender = customtkinter.CTkLabel(self.tabview.tab("Defender"), text="This is the defender tab")
        self.label_defender.grid(row=0, column=0, padx=20, pady=20)


    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)


if __name__ == "__main__":
    # Run app
    app = App()
    app.mainloop()