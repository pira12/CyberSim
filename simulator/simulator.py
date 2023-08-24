import globals as glob
import os
import customtkinter
from PIL import Image
from CTkMessagebox import CTkMessagebox
from event_handler import start_simulation, stop_simulation
from network import Network, Host, Edge

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

        self.defcost = customtkinter.CTkLabel(master=self.score_frame, text=f"Total{self.is_mult_runs()}score of the defender: {-1 * round(glob.def_total_cost/glob.NUM_SIMS, 1)}")
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
        self.title("NeDeS")
        self.geometry(f"{1366}x{768}")
        self.results_window = None
        self.protocol("WM_DELETE_WINDOW", self.quit)
        self.run_index = 0
        glob.created_network = Network()

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
        self.tabview.add("Create network")
        self.tabview.add("Actions")

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
        self.tabview.tab("Create network").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Actions").grid_columnconfigure(0, weight=1)

        """
        -------------------------------------------------------------------------------------------
        System tab
        """
        # The manual textbox
        self.textbox = customtkinter.CTkTextbox(self.tabview.tab("System"))
        self.textbox.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        temp_text = glob.manual
        self.textbox.insert("0.0", "Manual:\n" + temp_text)
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
        self.network_preview.grid(row=0, column=0, padx=10, pady=3, sticky="nsew")
        self.network_preview = customtkinter.CTkLabel(self.preview_frame, image=self.image, text="")
        self.network_preview.grid(row=1, column=0, padx=10, pady=3, sticky="nsew")

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


        """
        -------------------------------------------------------------------------------------------
        Create network tab
        """

        # Create the frame to create/delete hosts
        self.network_frame_host = customtkinter.CTkFrame(self.tabview.tab("Create network"))
        self.network_frame_host.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Create the frame to create/delete edges
        self.network_frame_edge = customtkinter.CTkFrame(self.tabview.tab("Create network"))
        self.network_frame_edge.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Create the frame to create/delete the sensitive hosts
        self.sensitive_frame = customtkinter.CTkFrame(self.tabview.tab("Create network"))
        self.sensitive_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")


        # The network preview frame
        self.create_network_frame = customtkinter.CTkFrame(self.tabview.tab("Create network"))
        self.create_network_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="nsew")

        self.update_preview_created_network()
        self.network_created_preview = customtkinter.CTkLabel(self.create_network_frame, text="Network selection preview:")
        self.network_created_preview.grid(row=0, column=0, padx=10, pady=3, sticky="nsew")
        self.network_created_preview = customtkinter.CTkLabel(self.create_network_frame, image=self.created_image, text="")
        self.network_created_preview.grid(row=1, column=0, padx=10, pady=3, sticky="nsew")

        # Add or delete a host to the network
        self.label_n2 = customtkinter.CTkLabel(master=self.network_frame_host, text="Set the address of the host:")
        self.label_n2.grid(row=1, column=0, padx=20, pady=20, sticky="nw")
        self.host_entry = customtkinter.CTkEntry(master=self.network_frame_host, placeholder_text="int, int")
        self.host_entry.grid(row=1, column=1, padx=(20, 20), pady=(20, 20), sticky="nw")

        self.label_n3 = customtkinter.CTkLabel(master=self.network_frame_host, text="Set score of the host:")
        self.label_n3.grid(row=2, column=0, padx=20, pady=20, sticky="nw")
        self.host_score = customtkinter.CTkEntry(master=self.network_frame_host, placeholder_text="int")
        self.host_score.grid(row=2, column=1, padx=(20, 20), pady=(20, 20), sticky="nw")

        self.label_n4 = customtkinter.CTkLabel(master=self.network_frame_host, text="Set the processes of the host:")
        self.label_n4.grid(row=3, column=0, padx=20, pady=20, sticky="nw")
        self.host_processes = customtkinter.CTkEntry(master=self.network_frame_host, placeholder_text="string, string, ..")
        self.host_processes.grid(row=3, column=1, padx=(20, 20), pady=(20, 20), sticky="nw")

        self.add_host_button = customtkinter.CTkButton(master=self.network_frame_host, text="Add host", command=self.add_host)
        self.add_host_button.grid(row=4, column=0, padx=20, pady=10)
        self.delete_host_button = customtkinter.CTkButton(master=self.network_frame_host, text="Delete host", command=self.delete_host)
        self.delete_host_button.grid(row=4, column=1, padx=20, pady=10)

        # Add or delete an edge to the network
        self.label_n5 = customtkinter.CTkLabel(master=self.network_frame_edge, text="Set the source address of the edge:")
        self.label_n5.grid(row=5, column=0, padx=20, pady=20, sticky="nw")
        self.edge_entry1 = customtkinter.CTkEntry(master=self.network_frame_edge, placeholder_text="int, int")
        self.edge_entry1.grid(row=5, column=1, padx=(20, 20), pady=(20, 20), sticky="nw")

        self.label_n6 = customtkinter.CTkLabel(master=self.network_frame_edge, text="Set the destination address of the edge:")
        self.label_n6.grid(row=6, column=0, padx=20, pady=20, sticky="nw")
        self.edge_entry2 = customtkinter.CTkEntry(master=self.network_frame_edge, placeholder_text="int, int")
        self.edge_entry2.grid(row=6, column=1, padx=(20, 20), pady=(20, 20), sticky="nw")

        self.label_n7 = customtkinter.CTkLabel(master=self.network_frame_edge, text="Set the services of the edge:")
        self.label_n7.grid(row=7, column=0, padx=20, pady=20, sticky="nw")
        self.edge_services = customtkinter.CTkEntry(master=self.network_frame_edge, placeholder_text="string, string, ..")
        self.edge_services.grid(row=7, column=1, padx=(20, 20), pady=(20, 20), sticky="nw")

        self.add_edge_button = customtkinter.CTkButton(master=self.network_frame_edge, text="Add edge", command=self.add_edge)
        self.add_edge_button.grid(row=8, column=0, padx=20, pady=10)
        self.delete_edge_button = customtkinter.CTkButton(master=self.network_frame_edge, text="Delete edge", command=self.delete_edge)
        self.delete_edge_button.grid(row=8, column=1, padx=20, pady=10)



        # Add or delete a sensitive host
        self.label_n8 = customtkinter.CTkLabel(master=self.sensitive_frame, text="Set the address of the sensitive host:")
        self.label_n8.grid(row=0, column=0, padx=20, pady=20, sticky="nw")
        self.sensitive_entry = customtkinter.CTkEntry(master=self.sensitive_frame, placeholder_text="int, int")
        self.sensitive_entry.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nw")

        self.add_sensitive_button = customtkinter.CTkButton(master=self.sensitive_frame, text="Add sensitive host", command=self.add_sensitive_host)
        self.add_sensitive_button.grid(row=1, column=0, padx=20, pady=10)
        self.delete_sensitive_button = customtkinter.CTkButton(master=self.sensitive_frame, text="Delete sensitive host", command=self.delete_sensitive_host)
        self.delete_sensitive_button.grid(row=1, column=1, padx=20, pady=10)

        self.use_created_network = customtkinter.CTkSwitch(master=self.sensitive_frame, text="Use created network")
        self.use_created_network.grid(row=2, column=0, padx=20, pady=20, sticky="W")
        glob.use_created_network = self.use_created_network


        """
        -------------------------------------------------------------------------------------------
        Actions tab
        """

        # Create the frame to create/delete hosts
        self.action_frame_attacks_h = customtkinter.CTkFrame(self.tabview.tab("Actions"))
        self.action_frame_attacks_h.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Create the frame to create/delete hosts
        self.action_frame_attacks_e = customtkinter.CTkFrame(self.tabview.tab("Actions"))
        self.action_frame_attacks_e.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.host_atrib1 = customtkinter.CTkLabel(master=self.action_frame_attacks_h, text="name")
        self.host_atrib1.grid(row=0, column=0, padx=20, pady=20, sticky="nw")
        self.host_atrib2 = customtkinter.CTkLabel(master=self.action_frame_attacks_h, text="cost")
        self.host_atrib2.grid(row=0, column=1, padx=20, pady=20, sticky="nw")
        self.host_atrib3 = customtkinter.CTkLabel(master=self.action_frame_attacks_h, text="duration")
        self.host_atrib3.grid(row=0, column=2, padx=20, pady=20, sticky="nw")
        self.host_atrib4 = customtkinter.CTkLabel(master=self.action_frame_attacks_h, text="process")
        self.host_atrib4.grid(row=0, column=3, padx=20, pady=20, sticky="nw")

        self.edge_atrib1 = customtkinter.CTkLabel(master=self.action_frame_attacks_e, text="name")
        self.edge_atrib1.grid(row=0, column=0, padx=20, pady=20, sticky="nw")
        self.edge_atrib2 = customtkinter.CTkLabel(master=self.action_frame_attacks_e, text="cost")
        self.edge_atrib2.grid(row=0, column=1, padx=20, pady=20, sticky="nw")
        self.edge_atrib3 = customtkinter.CTkLabel(master=self.action_frame_attacks_e, text="duration")
        self.edge_atrib3.grid(row=0, column=2, padx=20, pady=20, sticky="nw")
        self.edge_atrib4 = customtkinter.CTkLabel(master=self.action_frame_attacks_e, text="service")
        self.edge_atrib4.grid(row=0, column=3, padx=20, pady=20, sticky="nw")

        # Show the current attacks
        self.show_host_attacks()
        self.show_edge_attacks()


    def show_host_attacks(self):
        host_attacks = glob.atts_h

        for i in range(0, len(host_attacks)):
            self.temp1 = customtkinter.CTkLabel(master=self.action_frame_attacks_h, text=host_attacks[i].get_name())
            self.temp1.grid(row=i+1, column=0, padx=20, pady=20, sticky="nw")
            self.temp2 = customtkinter.CTkLabel(master=self.action_frame_attacks_h, text=host_attacks[i].get_cost())
            self.temp2.grid(row=i+1, column=1, padx=20, pady=20, sticky="nw")
            self.temp3 = customtkinter.CTkLabel(master=self.action_frame_attacks_h, text=host_attacks[i].get_duration())
            self.temp3.grid(row=i+1, column=2, padx=20, pady=20, sticky="nw")
            self.temp6 = customtkinter.CTkLabel(master=self.action_frame_attacks_h, text=host_attacks[i].get_process())
            self.temp6.grid(row=i+1, column=3, padx=20, pady=20, sticky="nw")


    def show_edge_attacks(self):
        edge_attacks = glob.atts_e

        for i in range(0, len(edge_attacks)):
            self.temp1 = customtkinter.CTkLabel(master=self.action_frame_attacks_e, text=edge_attacks[i].get_name())
            self.temp1.grid(row=i+1, column=0, padx=20, pady=20, sticky="nw")
            self.temp2 = customtkinter.CTkLabel(master=self.action_frame_attacks_e, text=edge_attacks[i].get_cost())
            self.temp2.grid(row=i+1, column=1, padx=20, pady=20, sticky="nw")
            self.temp3 = customtkinter.CTkLabel(master=self.action_frame_attacks_e, text=edge_attacks[i].get_duration())
            self.temp3.grid(row=i+1, column=2, padx=20, pady=20, sticky="nw")
            self.temp6 = customtkinter.CTkLabel(master=self.action_frame_attacks_e, text=edge_attacks[i].get_service())
            self.temp6.grid(row=i+1, column=3, padx=20, pady=20, sticky="nw")


    def process_address(self, input):
        """
        Check if the given input is of the format: int, int
        """
        addresses = input.split(",")
        if len(addresses) != 2:
            CTkMessagebox(master=app, title="Error", message="The address should be 'subnet address, host address'", icon="warning")
            return False, False

        addresses = [address.strip() for address in addresses]
        subnet_address = addresses[0]
        host_address = addresses[1]

        if subnet_address.isdigit() == False:
            CTkMessagebox(master=app, title="Error", message="The subnet address of the host must be a number", icon="warning")
            return False, False
        elif host_address.isdigit() == False:
            CTkMessagebox(master=app, title="Error", message="The host address of the host must be a number", icon="warning")
            return False, False

        return int(subnet_address), int(host_address)


    def add_host(self):
        """
        Add a host to the created network.
        """
        subnet_address, host_address = self.process_address(self.host_entry.get())
        host_processes = self.host_processes.get()
        host_processes = host_processes.split(",")
        host_processes = [process.strip() for process in host_processes]
        host_score = self.host_score.get()

        if subnet_address == False:
            return
        elif (subnet_address, host_address) in list(glob.created_network.host_map.keys()):
            CTkMessagebox(master=app, title="Error", message="The address of the host already exists", icon="warning")
        elif host_score.isdigit() == False:
            CTkMessagebox(master=app, title="Error", message="The score of the host must be a number", icon="warning")
        elif host_processes == ['']:
            CTkMessagebox(master=app, title="Error", message="The host must have at least one process", icon="warning")

        else:
            glob.created_network.add_host(Host(subnet_address, host_address, int(host_score), 2, 0, [], glob.hardware[0], host_processes, glob.services[0:1], glob.os[0]))
            self.update_preview_created_network()


    def delete_host(self):
        """
        Delete a host from the created network.
        """
        subnet_address, host_address = self.process_address(self.host_entry.get())

        if subnet_address == False:
            return
        elif (subnet_address, host_address) not in list(glob.created_network.host_map.keys()):
            CTkMessagebox(master=app, title="Error", message="The address of the host does not exist", icon="warning")
        elif (subnet_address, host_address) == (1, 0):
            CTkMessagebox(master=app, title="Error", message="The host (1, 0) is the internet and cannot be deleted", icon="warning")
        else:
            glob.created_network.delete_host((subnet_address, host_address))
            self.update_preview_created_network()


    def add_edge(self):
        """
        Add an edge to the created network.
        """
        source_subnet_address, source_host_address = self.process_address(self.edge_entry1.get())
        if source_subnet_address == False:
            return

        dest_subnet_address, dest_host_address = self.process_address(self.edge_entry2.get())
        if source_subnet_address == False or dest_subnet_address == False:
            return

        edge_services = self.edge_services.get()
        edge_services = edge_services.split(",")
        edge_services = [service.strip() for service in edge_services]
        print(edge_services[0] == "s1")

        if (source_subnet_address, source_host_address) not in list(glob.created_network.host_map.keys()):
            CTkMessagebox(master=app, title="Error", message="The source address of the edge does not exist", icon="warning")
        elif (dest_subnet_address, dest_host_address) not in list(glob.created_network.host_map.keys()):
            CTkMessagebox(master=app, title="Error", message="The destination address of the edge does not exist", icon="warning")
        elif (source_subnet_address, source_host_address) == (dest_subnet_address, dest_host_address):
            CTkMessagebox(master=app, title="Error", message="The edge has the same source and destination address", icon="warning")
        elif glob.created_network.check_edge_addr((source_subnet_address, source_host_address), (dest_subnet_address, dest_host_address)) == 1:
            CTkMessagebox(master=app, title="Error", message="This edge already exists", icon="warning")
        elif edge_services == ['']:
            CTkMessagebox(master=app, title="Error", message="The edge must have at least one service", icon="warning")
        else:
            glob.created_network.add_edge((source_subnet_address, source_host_address), (dest_subnet_address, dest_host_address), edge_services)
            self.update_preview_created_network()


    def delete_edge(self):
        """
        Delete an edge from the created network.
        """
        source_subnet_address, source_host_address = self.process_address(self.edge_entry1.get())
        if source_subnet_address == False:
            return
        dest_subnet_address, dest_host_address = self.process_address(self.edge_entry2.get())

        if source_subnet_address == False or dest_subnet_address == False:
            return
        elif (source_subnet_address, source_host_address) not in list(glob.created_network.host_map.keys()):
            CTkMessagebox(master=app, title="Error", message="The source address of the edge does not exist", icon="warning")
        elif (dest_subnet_address, dest_host_address) not in list(glob.created_network.host_map.keys()):
            CTkMessagebox(master=app, title="Error", message="The destination address of the edge does not exist", icon="warning")

        elif (source_subnet_address, source_host_address) == (dest_subnet_address, dest_host_address):
            CTkMessagebox(master=app, title="Error", message="The edge has the same source and destination address", icon="warning")
        elif glob.created_network.check_edge_addr((source_subnet_address, source_host_address), (dest_subnet_address, dest_host_address)) == 0:
            CTkMessagebox(master=app, title="Error", message="This edge does not exist", icon="warning")
        else:
            glob.created_network.delete_edge((source_subnet_address, source_host_address), (dest_subnet_address, dest_host_address))
            self.update_preview_created_network()


    def add_sensitive_host(self):
        """
        Change a host to a sensitive host.
        """
        subnet_address, host_address = self.process_address(self.sensitive_entry.get())

        if subnet_address == False:
            return
        elif (subnet_address, host_address) not in list(glob.created_network.host_map.keys()):
            CTkMessagebox(master=app, title="Error", message="The address of the edge does not exist", icon="warning")
        elif (subnet_address, host_address) in glob.created_network.sensitive_hosts:
            CTkMessagebox(master=app, title="Error", message="This address is already a sensitve host", icon="warning")
        else:
            glob.created_network.add_sensitive_hosts((subnet_address, host_address))
            CTkMessagebox(master=app, title="success", message="The sensitive host is added", icon="check")


    def delete_sensitive_host(self):
        """
        Change a sensitive host to a regular host.
        """
        subnet_address, host_address = self.process_address(self.sensitive_entry.get())

        if subnet_address == False:
            return
        elif (subnet_address, host_address) not in list(glob.created_network.host_map.keys()):
            CTkMessagebox(master=app, title="Error", message="The address of the edge does not exist", icon="warning")
        elif (subnet_address, host_address) not in glob.created_network.sensitive_hosts:
            CTkMessagebox(master=app, title="Error", message="This address is not a sensitve host", icon="warning")
        else:
            glob.created_network.delete_sensitive_hosts((subnet_address, host_address))
            CTkMessagebox(master=app, title="success", message="The sensitive host is deleted", icon="check")


    def show_success(self):
        """
        Function which will show the success pop-up box.
        """
        msg = CTkMessagebox(master=app, title="success", message="The simulation is done!", icon="check",
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
                                              size=(680,420))
        self.network_preview = customtkinter.CTkLabel(self.preview_frame, image=self.image, text="")
        self.network_preview.grid(row=1, column=0, padx=10, pady=3, sticky="nsew")
        glob.network_selection = self.network_options.get()

    def update_preview_created_network(self):
        """
        Function which will change the network preview according to the created network.
        """
        glob.created_network.draw_pre_attack_network()
        self.created_image = customtkinter.CTkImage(light_image=Image.open("created_network.png"),
                                              dark_image=Image.open("created_network.png"),
                                              size=(680,420))
        self.network_preview = customtkinter.CTkLabel(self.create_network_frame, image=self.created_image, text="")
        self.network_preview.grid(row=1, column=0, padx=10, pady=3, sticky="nsew")

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
        open('score_log.txt', 'w').close()
        glob.current_run = 0

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
        self.show_success()
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
