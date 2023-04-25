import enum

MAX_RUMTIME = 60

class AccessLevel(enum.IntEnum):
    NONE = 0
    USER = 1
    ROOT = 2

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class AttackStrat(enum.IntEnum):
    RANDOM = 0
    BRUTEF = 1

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class DefenseStrat(enum.IntEnum):
    RANDOM = 0
    BRUTEF = 1

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name