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

"""
Define logging settings.
"""
logging.basicConfig(filename='log.txt', filemode='w',
                    format='%(asctime)s %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

logging.basicConfig(filename='score_log.txt', filemode='w',
                    format='%(asctime)s %(message)s', level=logging.INFO)
score_logger = logging.getLogger(__name__)

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


atts_h = [PrivilegeEscalation("att_h1", 1, 10, 0.8, 1, process="p1"), PrivilegeEscalation("att_h2", 1, 10, 0.8, 1, process="p7")]
atts_e = [Exploit("att_e1", 1, 10, 0.8, service="s1"), Exploit("att_e2", 1, 10, 0.8, service="s1")]
hard_h = [Harden_host("harden att_h1", 1, 10, "att_h1"), Harden_host("harden att_h2", 1, 10, "att_h2"), Harden_host("harden att_h3", 1, 10, "att_h3")]
hard_e = [Harden_edge("harden att_e1", 1, 10, "att_e1"), Harden_edge("harden att_e2", 1, 10, "att_e2"), Harden_edge("harden att_e3", 1, 10, "att_e3")]


hardware = ["Lenovo"]
os = ["windows"]
services = ["s1", "s2"]
processes = ["p1", "p2"]
