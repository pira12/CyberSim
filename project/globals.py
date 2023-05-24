import enum
import logging
import os
os.environ['NUMEXPR_MAX_THREADS'] = '64'

from actions_def import Harden_host, Harden_edge
from actions_att import Exploit, PrivilegeEscalation



MAX_RUMTIME = 60
NUM_SIMS = 1
OUT_FILENAME = "output"

attacker_list= []
harden_host_allowed = None
harden_edge_allowed = None


"""
Define logging settings.
"""
logging.basicConfig(filename='log.txt', filemode='w',
                    format='%(asctime)s %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class AccessLevel(enum.IntEnum):
    NONE = 0
    USER = 1
    ROOT = 2

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class AttackStrat(enum.Enum):
    ZDE = "Zero-day exploit"
    APT = "Advanced Persistent Threats"
    DOS = "Denial Of Service"

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
