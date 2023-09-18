import enum
import logging
import os
os.environ['NUMEXPR_MAX_THREADS'] = '64'

from actions_def import Harden_host, Harden_edge
from actions_att import Exploit, PrivilegeEscalation


MAX_RUNTIME = 60
NUM_SIMS = 1
OUT_FOLDERNAME = "output"

attackers = []
progress_bar = None
network_selection = None
attacker_list= []
defender_strategy = None
harden_host_allowed = None
harden_edge_allowed = None
scan_host_allowed = None
update_host_allowed = None
update_firewall_allowed = None
created_network = None
use_created_network = None
current_run = 0

# Total score of all nodes
max_score = 0
# Total score of compromised nodes
compromised_score = 0
# Cost of all actions done
def_cost = 0
# Compromised score + def cost
def_total_cost = 0
# Attacker scores
att_scores = []
# Attacker costs
att_costs = []

"""
Define logging settings.
"""
formatter = logging.Formatter('%(asctime)s %(message)s')

def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# The action logger
logger = setup_logger('logger', 'log.txt')

# The score logger
score_logger = setup_logger('score_logger', 'score_log.txt')


class AccessLevel(enum.IntEnum):
    NONE = 0
    USER = 1
    ROOT = 2

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


atts_h = [PrivilegeEscalation("host_att1", 1, 10, 1, 1, process="p1"), PrivilegeEscalation("host_att2", 1, 10, 1, 1, process="p2")]
atts_e = [Exploit("edge_att1", 1, 10, 1, service="s1"), Exploit("edge_att2", 1, 10, 1, service="s2")]
hard_h = [Harden_host("harden host_att2", 1, 10, "host_att1"), Harden_host("harden host_att2", 1, 10, "host_att2")]
hard_e = [Harden_edge("harden edge_att1", 1, 10, "edge_att1"), Harden_edge("harden edge_att2", 1, 10, "edge_att2")]


hardware = ["Lenovo"]
os = ["windows"]
services = ["s1", "s2"]
processes = ["p1", "p2"]

manual = """
Settings sidebar:

    + Start button: This button will start the simulation when all the required fields are filled in correctly.

    + Results button: This button will show the results window when a simulation has finished running.

    + Appearance mode selector:
      This dropdown menu has three options:
        - Light: This option will show the GUI in light mode.
        - Dark: This option will show the GUI in dark mode.
        - System: This option will show the GUI in the mode your computer system is set on.

    + UI scaling selector: This dropdown menu has multiple options for scaling the simulator.
       These are 80%, 90%, 100%, 110%, and 120%.


Systems tab:

    + Network selector: This dropdown menu will show the available networks to run the simulation on.
       When selecting a network the network preview will change with it.

    + The number of simulations entry field: This entry field will decide how many times the simulation will be run. Must be an integer.

    + Simulation run time entry field: This entry field will decide how long the simulated time will be. Must be an integer.

    + Output folder name entry field: This entry field will decide the name of the output folder will be named, which contains all the results.


Create network tab:

    A custom network can be created by adding hosts and and edges to the network. The created network can be used by selecting
    'created_network' in the system tab.

    When adding hosts and edges, make sure there are attacks and hardenings that can be used on those processes and services.
    The default processes for which attacks and hardenings exist are p1 and p2, the default services are s1 and s2.


Attacker tab:

    On the attacker tab we create the number of attackers we want for a simulation,
    and then decide which strategy and which actions they should use.
    To create attackers, fill in an integer in the attacker entry field and follow that by pressing the create attackers button.
    The graphical user interface will now generate that amount of attackers in the scrollable frame.

    Each attacker has its own id. Each attacker can also be set with an attacker strategy by selecting it in the dropdown menu.
    The options are Random Strategy, Zero-day exploit, and Advanced Persistent Threats.

    You will notice that each strategy has actions which are blocked, these can not be unselected and will remain selected,
      the other actions however can be selected or unselected.


Defender tab:

    There is only one defender in the simulator therefore all the options for the defender are shown in this tab.

    First, the defender can choose its strategy by selecting one from the dropdown menu.
    These are the options for the defenders strategy:
    random, last layer, minimum, reactive and random, highest degree neighbour.

    The defender has split his actions into two parts. One part will affect the host and the other part will affect the edges between the hosts.
    The defender requires at least one defending action to be selected.


Log tab:

    The log tab displays the log for the latest simulation which has been finished running.


Results window

    The results window will show a quick summary of the results of the simulation.

    In the top left, we have the network topography after the simulation is finished.
    This topography will show which hosts have been compromised and which have not.

    Underneath that, we have the plot of the scores of the attacker(s) and defender over time.

    On the right side, there is a summary with all the valuable results from the simulation,
     which is divided into three parts: network, defender, and attacker.

    When the simulation is run multiple times, then the results will be shown in an average over all the simulations.
"""
