import tkinter
import globals as glob
import customtkinter
from CTkMessagebox import CTkMessagebox
from event_handler import start_simulation, stop_simulation

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
        # The manual textbox
        self.textbox = customtkinter.CTkTextbox(self.tabview.tab("System"))
        self.textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Create the frame for system settings
        self.option_frame = customtkinter.CTkFrame(self.tabview.tab("System"))
        self.option_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        self.tabview.tab("System").grid_rowconfigure(0, weight=3)
        self.option_frame.grid_columnconfigure(0, weight=3)
        self.textbox.grid_rowconfigure(0, weight=3)


        # Network selection
        self.label_1 = customtkinter.CTkLabel(master=self.option_frame, text="Select a network:")
        self.label_1.grid(row=0, column=0, padx=20, pady=20, sticky="nw")
        self.network_options = customtkinter.CTkOptionMenu(master=self.option_frame, dynamic_resizing=False,
                                                        values=["Network 1", "Network 2", "Network 3", "Network 4", "Network 5"])
        self.network_options.grid(row=0, column=1, padx=20, pady=(20, 20), sticky="nw")

        # Simulation number selection
        self.label_2 = customtkinter.CTkLabel(master=self.option_frame, text="Set the number of simulations:")
        self.label_2.grid(row=1, column=0, padx=20, pady=20, sticky="nw")
        self.sim_entry = customtkinter.CTkEntry(master=self.option_frame, placeholder_text="Number of simulations")
        self.sim_entry.grid(row=1, column=1, padx=(20, 20), pady=(20, 20), sticky="nw")

        # Runtime selection
        self.label_3 = customtkinter.CTkLabel(master=self.option_frame, text="Set the simulation run time:")
        self.label_3.grid(row=2, column=0, padx=20, pady=20, sticky="nw")
        self.time_entry = customtkinter.CTkEntry(master=self.option_frame, placeholder_text="Simulation time")
        self.time_entry.grid(row=2, column=1, padx=(20, 20), pady=(20, 20), sticky="nw")

        # Outpuf filename selection
        self.label_4 = customtkinter.CTkLabel(master=self.option_frame, text="Set the output file name:")
        self.label_4.grid(row=3, column=0, padx=20, pady=20, sticky="nw")
        self.file_entry = customtkinter.CTkEntry(master=self.option_frame, placeholder_text="Output filename")
        self.file_entry.grid(row=3, column=1, padx=(20, 20), pady=(20, 20), sticky="nw")

        # Selection for importing and saving settings
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
        # Upper frame for entry form.
        self.attacker_frame = customtkinter.CTkFrame(self.tabview.tab("Attacker"))
        self.attacker_frame.grid(row=0, column=0, padx=(10, 10), pady=(10,10), sticky="nsew")

        # Lower frame for generated attackers.
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self.tabview.tab("Attacker"), label_text="Attacker settings")
        self.scrollable_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.tabview.tab("Attacker").grid_rowconfigure(1, weight=3)
        self.scrollable_frame.grid_rowconfigure(1, weight=3)

        # Entry form with button to start function.
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
        # Frame for strategy
        self.defender_frame = customtkinter.CTkFrame(self.tabview.tab("Defender"))
        self.defender_frame.grid(row=0, column=0, padx=(10, 10), pady=(10,10), sticky="nsew")

        # Strategy selection.
        self.label_d1 = customtkinter.CTkLabel(master=self.defender_frame, text="Choose defence strategy:")
        self.label_d1.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.defense_strategy = customtkinter.CTkOptionMenu(master=self.defender_frame, dynamic_resizing=False,
                                                            values=["Strategy 1", "Strategy 2", "Strategy 3"])
        self.defense_strategy.grid(row=0, column=1, padx=10, pady=20)

        # Frame for edge actions
        self.edge_frame = customtkinter.CTkFrame(self.tabview.tab("Defender"))
        self.edge_frame.grid(row=1, column=0, padx=(10, 10), pady=(10,10), sticky="nsew")

        self.label_d2 = customtkinter.CTkLabel(master=self.edge_frame, text="Defender edge actions:")
        self.label_d2.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.harden_edge = customtkinter.CTkSwitch(master=self.edge_frame, text="Harden edge")
        self.harden_edge.grid(row=1, column=0, padx=20, pady=20, sticky="W")

        # Frame for host actions
        self.host_frame = customtkinter.CTkFrame(self.tabview.tab("Defender"))
        self.host_frame.grid(row=2, column=0, padx=(10, 10), pady=(10,10), sticky="nsew")

        self.label_d3 = customtkinter.CTkLabel(master=self.host_frame, text="Defender host actions:")
        self.label_d3.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.harden_host = customtkinter.CTkSwitch(master=self.host_frame, text="Harden host")
        self.harden_host.grid(row=1, column=0, padx=20, pady=20, sticky="W")

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
        """
        Function connected to the start button.
        """
        if self.check_edge_cases() == True:
            return
        start_simulation()

    def stop_event(self):
        print("Stop simulation")

    def results_event(self):
        print("Show results")

    def set_attackers(self):
        """ Function which generates attacker frames based on input from entry form."""
        glob.attacker_list = [[] for _ in range(int(self.att_entry.get()))]
        for i in range(int(self.att_entry.get())):
            # Creates a form and splits it in rows of 2.
            self.attacker_frame = customtkinter.CTkFrame(master=self.scrollable_frame)
            self.attacker_frame.grid(row=i//2, column=i%2, padx=(10, 10), pady=(10,10), sticky="nsew")

            self.label_attacker = customtkinter.CTkLabel(master=self.attacker_frame, text=f"Attacker {i}")
            self.label_attacker.grid(row=0, column=0, padx=10, pady=10, sticky="W")

            # Strategy for attacker
            strategy = customtkinter.CTkOptionMenu(master=self.attacker_frame, dynamic_resizing=False,
                                                        values=["Strategy 1", "Strategy 2", "Strategy 3"])
            strategy.grid(row=0, column=1, padx=10, pady=20)
            glob.attacker_list[i].append(strategy)

            # List with actions
            switch = customtkinter.CTkSwitch(master=self.attacker_frame, text="Subnet Scan")
            switch.grid(row=1, column=0, padx=10, pady=20, sticky="W")
            glob.attacker_list[i].append(switch)

            switch = customtkinter.CTkSwitch(master=self.attacker_frame, text="Operating System Scan")
            switch.grid(row=2, column=0, padx=10, pady=20, sticky="W")
            glob.attacker_list[i].append(switch)

            switch = customtkinter.CTkSwitch(master=self.attacker_frame, text="Hardware Scan")
            switch.grid(row=3, column=0, padx=10, pady=20, sticky="W")
            glob.attacker_list[i].append(switch)

            switch = customtkinter.CTkSwitch(master=self.attacker_frame, text="Process Scan")
            switch.grid(row=4, column=0, padx=10, pady=20, sticky="W")
            glob.attacker_list[i].append(switch)

            switch = customtkinter.CTkSwitch(master=self.attacker_frame, text="Service Scan")
            switch.grid(row=1, column=1, padx=10, pady=20, sticky="W")
            glob.attacker_list[i].append(switch)

            switch = customtkinter.CTkSwitch(master=self.attacker_frame, text="Exploit")
            switch.grid(row=2, column=1, padx=10, pady=20, sticky="W")
            glob.attacker_list[i].append(switch)

            switch = customtkinter.CTkSwitch(master=self.attacker_frame, text="Privilege Escalation")
            switch.grid(row=3, column=1, padx=10, pady=20, sticky="W")
            glob.attacker_list[i].append(switch)

    def check_edge_cases(self):
        """
        Funciton which checks if everything is filled in before running the simualtion.
        """
        if self.sim_entry.get() == "":
            CTkMessagebox(master=app, title="Error", message="The number of simulations is not set!", icon="warning")
            return True
        else:
            glob.NUM_SIMS = self.sim_entry.get()

        if self.time_entry.get() == "":
            CTkMessagebox(master=app, title="Error", message="The simulation time entry is empty!", icon="warning")
            return True
        else:
            glob.MAX_RUNTIME = self.time_entry.get()

        if self.file_entry.get() == "":
            CTkMessagebox(master=app, title="Error", message="The output filename is not chosen!", icon="warning")
            return True
        else:
            glob.OUT_FILENAME = self.file_entry.get()

        if self.att_entry.get() == "" or len(glob.attacker_list) <= 0:
            CTkMessagebox(master=app, title="Error", message="There not enough attakers generated!", icon="warning")
            return True

        for i, attacker in enumerate(glob.attacker_list):
            switch_check = 0
            for switch in attacker:
                if switch.get() == 1:
                    switch_check += 1
            if switch_check == 0:
                CTkMessagebox(master=app, title="Error", message=f"Select at least one attack for attacker {i}!", icon="warning")
                return True

        if self.harden_edge.get() == 0 and self.harden_host.get() == 0:
            CTkMessagebox(master=app, title="Error", message="Select at least one defence method for the defender!", icon="warning")
            return True

if __name__ == "__main__":
    # Run app
    app = App()
    app.mainloop()