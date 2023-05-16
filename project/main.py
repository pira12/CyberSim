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

        self.sidebar_start = customtkinter.CTkButton(self.sidebar_frame, text="Start", command=self.start_event)
        self.sidebar_start.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_stop = customtkinter.CTkButton(self.sidebar_frame, text="Stop", command=self.stop_event)
        self.sidebar_stop.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_results = customtkinter.CTkButton(self.sidebar_frame, text="Results", command=self.results_event)
        self.sidebar_results.grid(row=3, column=0, padx=20, pady=10)

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
        self.textbox = customtkinter.CTkTextbox(self.tabview.tab("System"), width=440)
        self.textbox.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.option_frame = customtkinter.CTkFrame(self.tabview.tab("System"), width=440)
        self.option_frame.grid(row=0, column=1, padx=(20, 20), pady=(20,20), sticky="nsew")

        self.label_1 = customtkinter.CTkLabel(master=self.option_frame, text="Select a network:")
        self.label_1.grid(row=0, column=0, padx=20, pady=20)
        self.network_options = customtkinter.CTkOptionMenu(master=self.option_frame, dynamic_resizing=False,
                                                        values=["Network 1", "Network 2", "Network 3", "Network 4", "Network 5"])
        self.network_options.grid(row=0, column=1, padx=20, pady=(20, 20))

        self.label_2 = customtkinter.CTkLabel(master=self.option_frame, text="Set the number of simulations:")
        self.label_2.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.sim_entry = customtkinter.CTkEntry(master=self.option_frame, placeholder_text="Number of simulations")
        self.sim_entry.grid(row=1, column=1, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.label_3 = customtkinter.CTkLabel(master=self.option_frame, text="Set the simulation run time:")
        self.label_3.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        self.time_entry = customtkinter.CTkEntry(master=self.option_frame, placeholder_text="Simulation time")
        self.time_entry.grid(row=2, column=1, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.label_4 = customtkinter.CTkLabel(master=self.option_frame, text="Set the output file name:")
        self.label_4.grid(row=3, column=0, padx=20, pady=20, sticky="nsew")
        self.file_entry = customtkinter.CTkEntry(master=self.option_frame, placeholder_text="Output filename")
        self.file_entry.grid(row=3, column=1, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # self.label_5 = customtkinter.CTkLabel(master=self.option_frame, text="Import Configuration:")
        # self.label_5.grid(row=4, column=0, padx=20, pady=20, sticky="nsew")
        # self.entry = customtkinter.CTkEntry(master=self.option_frame, placeholder_text="Output filename")
        # self.entry.grid(row=4, column=1, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # self.label_6 = customtkinter.CTkLabel(master=self.option_frame, text="Save configurations:")
        # self.label_6.grid(row=5, column=0, padx=20, pady=20, sticky="nsew")
        # self.entry = customtkinter.CTkEntry(master=self.option_frame, placeholder_text="Output filename")
        # self.entry.grid(row=5, column=1, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        """
        -------------------------------------------------------------------------------------------
        Attacker tab
        """
        self.attacker_frame = customtkinter.CTkFrame(self.tabview.tab("Attacker"))
        self.attacker_frame.grid(row=0, column=0, padx=(10, 10), pady=(10,10), sticky="nsew")

        self.scrollable_frame = customtkinter.CTkScrollableFrame(self.tabview.tab("Attacker"), label_text="Attacker settings")
        self.scrollable_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.tabview.tab("Attacker").grid_rowconfigure(1, weight=3)
        self.scrollable_frame.grid_rowconfigure(1, weight=3)

        self.label_a1 = customtkinter.CTkLabel(master=self.attacker_frame, text="Set number of attackers:")
        self.label_a1.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.att_entry = customtkinter.CTkEntry(master=self.attacker_frame, placeholder_text="Number of attackers")
        self.att_entry.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.set_attackers = customtkinter.CTkButton(master=self.attacker_frame, text="Create attackers", command=self.set_attackers)
        self.set_attackers.grid(row=0, column=2, padx=20, pady=10)

        """
        -------------------------------------------------------------------------------------------
        Defender tab
        """
        self.label_defender = customtkinter.CTkLabel(self.tabview.tab("Defender"), text="This is the defender tab")
        self.label_defender.grid(row=0, column=0, padx=20, pady=20)

        """
        -------------------------------------------------------------------------------------------
        Set the deafult values
        """
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.textbox.insert("0.0", "Manual?\n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)


    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def start_event(self):
        print("Start simulation")

    def stop_event(self):
        print("Stop simulation")

    def results_event(self):
        print("Show results")

    def set_attackers(self):
        for i in range(int(self.att_entry.get())):
            self.attacker_frame = customtkinter.CTkFrame(master=self.scrollable_frame)
            self.attacker_frame.grid(row=i//2, column=i%2, padx=(10, 10), pady=(10,10), sticky="nsew")
            self.attacker_frame_switches = []

            self.label_attacker = customtkinter.CTkLabel(master=self.attacker_frame, text=f"Attacker {i}")
            self.label_attacker.grid(row=0, column=0, padx=10, pady=10, sticky="W")

            switch = customtkinter.CTkSwitch(master=self.attacker_frame, text="Subnet Scan")
            switch.grid(row=1, column=0, padx=10, pady=20, sticky="W")
            self.attacker_frame_switches.append(switch)

            switch = customtkinter.CTkSwitch(master=self.attacker_frame, text="Operating System Scan")
            switch.grid(row=2, column=0, padx=10, pady=20, sticky="W")
            self.attacker_frame_switches.append(switch)

            switch = customtkinter.CTkSwitch(master=self.attacker_frame, text="Hardware Scan")
            switch.grid(row=3, column=0, padx=10, pady=20, sticky="W")
            self.attacker_frame_switches.append(switch)

            switch = customtkinter.CTkSwitch(master=self.attacker_frame, text="Process Scan")
            switch.grid(row=4, column=0, padx=10, pady=20, sticky="W")
            self.attacker_frame_switches.append(switch)

            switch = customtkinter.CTkSwitch(master=self.attacker_frame, text="Service Scan")
            switch.grid(row=1, column=1, padx=10, pady=20, sticky="W")
            self.attacker_frame_switches.append(switch)

            switch = customtkinter.CTkSwitch(master=self.attacker_frame, text="Exploit")
            switch.grid(row=2, column=1, padx=10, pady=20, sticky="W")
            self.attacker_frame_switches.append(switch)

            switch = customtkinter.CTkSwitch(master=self.attacker_frame, text="Privilege Escalation")
            switch.grid(row=3, column=1, padx=10, pady=20, sticky="W")
            self.attacker_frame_switches.append(switch)


if __name__ == "__main__":
    # Run app
    app = App()
    app.mainloop()