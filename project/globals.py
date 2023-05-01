import enum
import logging

MAX_RUMTIME = 60

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


class AttackStrat(enum.IntEnum):
    RAND = 0
    AGRO = 1
    DEFF = 2

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
