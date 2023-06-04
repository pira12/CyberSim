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

# Total score of all nodes
max_score = None
# Total score of compromised nodes
compromised_score = None
# Cost of all actions done
def_cost = None
# Compromised score + def cost
def_total_cost = None

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

# logging.basicConfig(filename='log.txt', filemode='w',
#                     format='%(asctime)s %(message)s', level=logging.INFO)
# logger = logging.getLogger(__name__)


class AccessLevel(enum.IntEnum):
    NONE = 0
    USER = 1
    ROOT = 2

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class AttackStrat(enum.Enum):
    RST = "Random Strategy"
    ZDE = "Zero-day exploit"
    APT = "Advanced Persistent Threats"

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class DefenseStrat(enum.IntEnum):
    RAND = 0
    AGRO = 1
    DEFF = 2

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


atts_h = [PrivilegeEscalation("host_att1", 1, 10, 0.8, 1, process="p1"), PrivilegeEscalation("host_att2", 1, 10, 0.8, 1, process="p7")]
atts_e = [Exploit("edge_att1", 1, 10, 0.8, service="s1"), Exploit("edge_att2", 1, 10, 0.8, service="s2")]
hard_h = [Harden_host("harden host_att2", 1, 10, "host_att1"), Harden_host("harden host_att2", 1, 10, "host_att2")]
hard_e = [Harden_edge("harden edge_att1", 1, 10, "edge_att1"), Harden_edge("harden edge_att2", 1, 10, "edge_att2")]


hardware = ["Lenovo"]
os = ["windows"]
services = ["s1", "s2"]
processes = ["p1", "p2"]
