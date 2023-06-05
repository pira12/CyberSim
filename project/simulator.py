import globals as glob
import os
import customtkinter
from PIL import Image
from CTkMessagebox import CTkMessagebox
from event_handler import start_simulation, stop_simulation

# System appearance settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class ResultsWindow(customtkinter.CTkToplevel):
    """
    This class is made for the results window.
    """
    def __init__(self):
        super().__init__()
        self.geometry(f"{1000}x{640}")
        self.title("Results Window")

        # Import the image in the window for the network.
        self.result_image = customtkinter.CTkImage(light_image=Image.open(f"./{glob.OUT_FOLDERNAME}/Network_fig.png"),
                                                   dark_image=Image.open(f"./{glob.OUT_FOLDERNAME}/Network_fig.png"),
                                                   size=(600, 300))
        self.result_preview = customtkinter.CTkLabel(self, image=self.result_image, text="")
        self.result_preview.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        # Import the image in the window for the graph.
        self.result_image = customtkinter.CTkImage(light_image=Image.open(f"./{glob.OUT_FOLDERNAME}/Plot_fig.png"),
                                                   dark_image=Image.open(f"./{glob.OUT_FOLDERNAME}/Plot_fig.png"),
                                                   size=(600, 300))
        self.result_preview = customtkinter.CTkLabel(self, image=self.result_image, text="")
        self.result_preview.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

        # Create a frame for the score results.
        self.score_frame = customtkinter.CTkScrollableFrame(self, width=360, corner_radius=5)
        self.score_frame.grid(row=0, column=1, rowspan=4, padx=5, pady=10, sticky="nsew")
        self.score_frame.grid_rowconfigure(4, weight=1)

        # Add all the results in labels.
        self.logo_label = customtkinter.CTkLabel(self.score_frame, text="Network:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=10, sticky="nw")

        self.maxscore = customtkinter.CTkLabel(master=self.score_frame, text=f"Total{self.is_mult_runs()}score of all hosts: {round(glob.max_score/glob.NUM_SIMS, 1)}")
        self.maxscore.grid(row=1, column=0, padx=20, pady=5, sticky="nw")

        self.compscore = customtkinter.CTkLabel(master=self.score_frame, text=f"Total{self.is_mult_runs()}score of compromised hosts: {round(glob.compromised_score/glob.NUM_SIMS, 1)}")
        self.compscore.grid(row=2, column=0, padx=20, pady=5, sticky="nw")

        self.logo_label = customtkinter.CTkLabel(self.score_frame, text="Defender:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=3, column=0, padx=20, pady=10, sticky="nw")

        self.defcost = customtkinter.CTkLabel(master=self.score_frame, text=f"Total{self.is_mult_runs()}cost of the defender: {round(glob.def_cost/glob.NUM_SIMS, 1)}")
        self.defcost.grid(row=4, column=0, padx=20, pady=5, sticky="nw")

        self.defcost = customtkinter.CTkLabel(master=self.score_frame, text=f"Total{self.is_mult_runs()}loss of the defender: {round(glob.def_total_cost/glob.NUM_SIMS, 1)}")
        self.defcost.grid(row=5, column=0, padx=20, pady=5, sticky="nw")

        self.logo_label = customtkinter.CTkLabel(self.score_frame, text="Attacker:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=6, column=0, padx=20, pady=10, sticky="nw")

        for i in range(len(glob.att_scores)):
            self.attack_score = customtkinter.CTkLabel(master=self.score_frame, text=f"Total{self.is_mult_runs()}score of attacker {i}: {round(glob.att_scores[i]/glob.NUM_SIMS, 1)}")
            self.attack_score.grid(row=7+2*i, column=0, padx=20, pady=5, sticky="nw")

            self.attack_cost = customtkinter.CTkLabel(master=self.score_frame, text=f"Total{self.is_mult_runs()}cost of  attacker {i}: {round(glob.att_costs[i]/glob.NUM_SIMS, 1)}")
            self.attack_cost.grid(row=8+2*i, column=0, padx=20, pady=5, sticky="nw")

    def is_mult_runs(self):
        """
        Function which will check if there are multiple runs and if there are return average else 1 space.
        """
        if glob.NUM_SIMS > 1:
            return " average "
        else:
            return " "


class App(customtkinter.CTk):
    """
    This class is made for the main GUI window and is split in parts.
    """
    def __init__(self):
        super().__init__()
        """
        Window configuration
        """
        self.title("Cyber Security Simulator")
        self.geometry(f"{1100}x{580}")
        self.results_window = None
        self.protocol("WM_DELETE_WINDOW", self.quit)
        self.run_index = 0

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
        # Creating the sidebar frame.
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Adding a logo/text to the sidebar.
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Simulator settings", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Adding buttons to the sidebar.
        self.sidebar_start = customtkinter.CTkButton(self.sidebar_frame, text="Start", command=self.start_event)
        self.sidebar_start.grid(row=1, column=0, padx=20, pady=10)
        # self.sidebar_stop = customtkinter.CTkButton(self.sidebar_frame, text="Stop", command=self.stop_event)
        # self.sidebar_stop.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_results = customtkinter.CTkButton(self.sidebar_frame, text="Results", command=self.results_event, state="disabled")
        self.sidebar_results.grid(row=3, column=0, padx=20, pady=10)

        # Adding a selection tool for the appearance mode and the scale.
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

        # Set the deafult values.
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

        """
        -------------------------------------------------------------------------------------------
        Main frame
        """
        # Creating a switchable tab frame for the main frame.
        self.tabview = customtkinter.CTkTabview(self, width=880, height=550)
        self.tabview.grid(row=0, column=1, columnspan=4, rowspan=4, padx=5, pady=5, sticky="nesw")
        self.tabview.add("System")
        self.tabview.add("Attacker")
        self.tabview.add("Defender")
        self.tabview.add("Simulation log")

        self.progressbar = customtkinter.CTkProgressBar(self, orientation="horizontal", height=5)
        self.progressbar.grid(row=2, column=1, columnspan=4, padx=5, pady=5, sticky="esw")
        self.progressbar.set(0)
        glob.progress_bar = self.progressbar

        """
        -------------------------------------------------------------------------------------------
        Configure grid of individual tabs
        """
        self.tabview.tab("System").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Attacker").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Defender").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Simulation log").grid_columnconfigure(0, weight=1)

        """
        -------------------------------------------------------------------------------------------
        System tab
        """
        # The manual textbox
        self.textbox = customtkinter.CTkTextbox(self.tabview.tab("System"))
        self.textbox.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        self.textbox.insert("0.0", "Manual?\n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)
        self.textbox.configure(state="disabled")

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
                                                           values=["network1", "network2", "network3", "network4", "network5"],
                                                           command=self.update_network_entry)
        self.network_options.grid(row=0, column=1, padx=20, pady=(20, 20), sticky="nw")

        # The network preview frame
        self.preview_frame = customtkinter.CTkFrame(self.tabview.tab("System"))
        self.preview_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.update_network_entry(0)
        self.network_preview = customtkinter.CTkLabel(self.preview_frame, text="Network selection preview:")
        self.network_preview.grid(row=0, column=0, padx=10, pady=2.5, sticky="nsew")
        self.network_preview = customtkinter.CTkLabel(self.preview_frame, image=self.image, text="")
        self.network_preview.grid(row=1, column=0, padx=10, pady=2.5, sticky="nsew")

        # Simulation number selection
        self.label_2 = customtkinter.CTkLabel(master=self.option_frame, text="Set the number of simulations:")
        self.label_2.grid(row=1, column=0, padx=20, pady=20, sticky="nw")
        self.sim_entry = customtkinter.CTkEntry(master=self.option_frame, placeholder_text="Number of simulations")
        self.sim_entry.grid(row=1, column=1, padx=(20, 20), pady=(20, 20), sticky="nw")

        # Runtime selection
        self.label_3 = customtkinter.CTkLabel(master=self.option_frame, text="Set the simulation run time:")
        self.label_3.grid(row=2, column=0, padx=20, pady=20, sticky="nw")
        self.runtime = customtkinter.CTkEntry(master=self.option_frame, placeholder_text="Simulation time")
        self.runtime.grid(row=2, column=1, padx=(20, 20), pady=(20, 20), sticky="nw")

        # Outpuf filename selection
        self.label_4 = customtkinter.CTkLabel(master=self.option_frame, text="Set the output folder name:")
        self.label_4.grid(row=3, column=0, padx=20, pady=20, sticky="nw")
        self.folder_entry = customtkinter.CTkEntry(master=self.option_frame, placeholder_text="Folder name")
        self.folder_entry.grid(row=3, column=1, padx=(20, 20), pady=(20, 20), sticky="nw")

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

        # Make the frames fill the empty spaces.
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
                                                            values=["random", "last layer", "minimum", "reactive and random", "highest degree neighbour"])
        self.defense_strategy.grid(row=0, column=1, padx=10, pady=20)
        glob.defender_strategy = self.defense_strategy

        # Frame for edge actions
        self.edge_frame = customtkinter.CTkFrame(self.tabview.tab("Defender"))
        self.edge_frame.grid(row=1, column=0, padx=(10, 10), pady=(10,10), sticky="nsew")

        self.label_d2 = customtkinter.CTkLabel(master=self.edge_frame, text="Defender edge actions:")
        self.label_d2.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.harden_edge = customtkinter.CTkSwitch(master=self.edge_frame, text="Harden edge")
        self.harden_edge.grid(row=1, column=0, padx=20, pady=20, sticky="W")
        self.harden_edge.select()
        glob.harden_edge_allowed = self.harden_edge

        self.update_firewall = customtkinter.CTkSwitch(master=self.edge_frame, text="Update firewall")
        self.update_firewall.grid(row=1, column=1, padx=20, pady=20, sticky="W")
        self.update_firewall.select()
        glob.update_firewall_allowed = self.update_firewall

        # Frame for host actions
        self.host_frame = customtkinter.CTkFrame(self.tabview.tab("Defender"))
        self.host_frame.grid(row=2, column=0, padx=(10, 10), pady=(10,10), sticky="nsew")

        self.label_d3 = customtkinter.CTkLabel(master=self.host_frame, text="Defender host actions:")
        self.label_d3.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.harden_host = customtkinter.CTkSwitch(master=self.host_frame, text="Harden host")
        self.harden_host.grid(row=1, column=0, padx=20, pady=20, sticky="W")
        self.harden_host.select()
        glob.harden_host_allowed = self.harden_host

        self.scan_host = customtkinter.CTkSwitch(master=self.host_frame, text="Scan host")
        self.scan_host.grid(row=1, column=1, padx=20, pady=20, sticky="W")
        self.scan_host.select()
        glob.scan_host_allowed = self.scan_host

        self.update_host = customtkinter.CTkSwitch(master=self.host_frame, text="Update host")
        self.update_host.grid(row=1, column=2, padx=20, pady=20, sticky="W")
        self.update_host.select()
        glob.update_host_allowed = self.update_host

        """
        -------------------------------------------------------------------------------------------
        Simulation log tab
        """
        # The manual textbox
        self.log = customtkinter.CTkTextbox(self.tabview.tab("Simulation log"))
        self.log.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.log.insert("0.0", "This is where the log will appear after the simulation...")
        self.log.configure(state="disabled")

        # Make the frames fill the empty spaces.
        self.tabview.tab("Simulation log").grid_rowconfigure(0, weight=3)
        self.log.grid_rowconfigure(0, weight=3)

    def show_succes(self):
        """
        Function which will show the succes pop-up box.
        """
        msg = CTkMessagebox(master=app, title="Succes", message="The simulation is done!", icon="check",
                            option_1="Thanks", option_2="Show results")

        if msg.get()=="Show results":
            self.results_event()


    def change_appearance_mode_event(self, new_appearance_mode: str):
        """
        Function which will change the appearance of the GUI.
        """
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        """
        Function which will change the scaling of the GUI.
        """
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def update_network_entry(self, dummy):
        """
        Function which will change the network preview according to its selction.
        """
        self.image = customtkinter.CTkImage(light_image=Image.open(f"basic_networks/basic_{self.network_options.get()}.png"),
                                              dark_image=Image.open(f"basic_networks/basic_{self.network_options.get()}.png"),
                                              size=(420,225))
        self.network_preview = customtkinter.CTkLabel(self.preview_frame, image=self.image, text="")
        self.network_preview.grid(row=1, column=0, padx=10, pady=2.5, sticky="nsew")
        glob.network_selection = self.network_options.get()

    def reset_results(self):
        """
        Function which will reset the result values between runs.
        """
        glob.max_score = 0
        glob.compromised_score = 0
        glob.def_cost = 0
        glob.def_total_cost = 0
        glob.att_scores = []
        glob.att_costs = []

    def start_event(self):
        """
        Function connected to the start button.
        """
        self.reset_results()

        open("log.txt", 'w').close()

        self.progressbar.set(0)
        if self.check_edge_cases() == True:
            return

        if glob.NUM_SIMS > 1:
            for i in range(0, glob.NUM_SIMS):
                start_simulation()
                self.run_index += 1
        else:
            start_simulation()
            self.run_index += 1

        # Update the log to the GUI.
        self.log.configure(state="normal")
        if self.run_index == 1:
            self.log.delete("0.0","end")
        with open("log.txt") as f:
            log = f.read()

        self.log.delete("0.0","end")
        self.log.insert("0.0", f" SIMULATION RUN {self.run_index}\n-----------------------------\n{log}\n\n")
        self.log.configure(state="disabled")

        os.system(f"cp ./log.txt ./{glob.OUT_FOLDERNAME}/log.txt")
        os.system(f"cp ./score_log.txt ./{glob.OUT_FOLDERNAME}/score_log.txt")

        self.progressbar.set(1)
        self.show_succes()
        self.sidebar_results.configure(state="normal")

    def stop_event(self):
        print("Stop simulation")

    def results_event(self):
        """
        Function which will show the resuls by spawning a  results window.
        """
        if self.results_window is None or not self.results_window.winfo_exists():
            self.results_window = ResultsWindow()  # create window if its None or destroyed
        else:
            self.results_window.focus()  # if window exists focus it

    def set_attackers(self):
        """
        Function which generates attacker frames based on input from entry form.
        """
        if self.att_entry.get() == "":
            CTkMessagebox(master=app, title="Error", message="Choose number of attackers!", icon="warning")
            return True

        if self.att_entry.get().isdigit() == False:
            CTkMessagebox(master=app, title="Error", message="The input for number of attackers is not a number!", icon="warning")
            return True

        glob.attacker_list = [[] for _ in range(int(self.att_entry.get()))]
        for widgets in self.scrollable_frame.winfo_children():
            widgets.destroy()

        for i in range(int(self.att_entry.get())):
            # Creates a frame and splits it in rows of 2.
            self.attacker_frame = customtkinter.CTkFrame(master=self.scrollable_frame)
            self.attacker_frame.grid(row=i//2, column=i%2, padx=(10, 10), pady=(10,10), sticky="nsew")

            self.label_attacker = customtkinter.CTkLabel(master=self.attacker_frame, text=f"Attacker {i}")
            self.label_attacker.grid(row=0, column=0, padx=10, pady=10, sticky="W")

            # Strategy for attacker
            strategy = customtkinter.CTkOptionMenu(master=self.attacker_frame, dynamic_resizing=False,
                                                        values=["Random Strategy", "Zero-day exploit", "Advanced Persistent Threats"])
            strategy.grid(row=0, column=1, padx=10, pady=20)
            glob.attacker_list[i].append(strategy)

            # List with actions
            switch = customtkinter.CTkSwitch(master=self.attacker_frame, text="Subnet Scan")
            switch.grid(row=1, column=0, padx=10, pady=20, sticky="W")
            switch.select()
            switch.configure(state="disabled")
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
            switch.select()
            switch.configure(state="disabled")
            glob.attacker_list[i].append(switch)

            switch = customtkinter.CTkSwitch(master=self.attacker_frame, text="Privilege Escalation")
            switch.grid(row=3, column=1, padx=10, pady=20, sticky="W")
            switch.select()
            switch.configure(state="disabled")
            glob.attacker_list[i].append(switch)

            switch = customtkinter.CTkSwitch(master=self.attacker_frame, text="Denial Of Service")
            switch.grid(row=4, column=1, padx=10, pady=20, sticky="W")
            glob.attacker_list[i].append(switch)

    def check_edge_cases(self):
        """
        Funciton which checks if everything is filled in before running the simualtion.
        """
        if self.sim_entry.get() == "":
            CTkMessagebox(master=app, title="Error", message="The number of simulations is not set!", icon="warning")
            return True
        elif int(self.sim_entry.get()) <= 0:
            CTkMessagebox(master=app, title="Error", message="The input for number of simulations must be higher than 0!", icon="warning")
            return True
        elif self.sim_entry.get().isdigit() == False:
            CTkMessagebox(master=app, title="Error", message="The input for number of simulations is not a number!", icon="warning")
            return True
        else:
            glob.NUM_SIMS = int(self.sim_entry.get())

        if self.runtime.get() == "":
            CTkMessagebox(master=app, title="Error", message="The simulation time entry is empty!", icon="warning")
            return True
        elif int(self.runtime.get()) <= 0:
            CTkMessagebox(master=app, title="Error", message="The input for max runtime must be higher than 0!", icon="warning")
            return True
        elif self.runtime.get().isdigit() == False:
            CTkMessagebox(master=app, title="Error", message="The input for max runtime is not a number!", icon="warning")
            return True
        else:
            glob.MAX_RUNTIME = self.runtime.get()

        if self.folder_entry.get() == "":
            CTkMessagebox(master=app, title="Error", message="The output filename is not chosen!", icon="warning")
            return True
        else:
            glob.OUT_FOLDERNAME = self.folder_entry.get()
            try:
                os.mkdir(f"./{self.folder_entry.get()}")
            except FileExistsError:
                pass

        if self.att_entry.get().isdigit() == False:
            CTkMessagebox(master=app, title="Error", message="The input for number of attackers is not a number!", icon="warning")
            return True
        elif self.att_entry.get() == "" or len(glob.attacker_list) <= 0:
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
    os.remove("./log.txt")
    os.remove("./score_log.txt")
