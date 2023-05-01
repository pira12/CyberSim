from globals import AccessLevel

"""
**Actions:**

Every action inherits from the base :class:`Action` class, which defines
some common attributes and functions. Different types of actions
are implemented as subclasses of the Action class.

Attacker action types implemented:

- :class:`Exploit`
- :class:`PrivilegeEscalation`
- :class:`SubnetScan`
- :class:`OSScan`
- :class:`HardwareScan`
- :class:`ProcessScan`
- :class:`ServiceScan`

"""


class Action:
    """
    The base action classs for Attack actions and Defender actions.
    ...
    Attributes
    ----------
    name : str
        The name of action
    target : (int, int)
        The (subnet, host) address of target of the action. The target of the
        action could be the address of a host that the action is being used
        against or could be the host that the action is being executed on.
    cost : float
        The cost of performing the action.
    duration : float
        The time it takes for the action to finish.
    prob : float
        The success probability of the action. This is the probability that
        the action works given that it's preconditions are met.
    req_access : AccessLevel,
        The required access level to perform action.
    """

    def __init__(self,
                 name,
                 target,
                 cost,
                 duration,
                 prob=1.0,
                 req_access=AccessLevel.USER):

        self.name = name
        self.target = target
        self.cost = cost
        self.duration = duration
        self.prob = prob
        self.req_access = req_access


class Exploit(Action):
    """
    Exploit action and inherits base action from the Action Class.

    ...

    Attributes
    ----------
    hardware: str
        The hardware which is targeted by the exploit.
        If none it works it works for all.
    os: str
        The operating system which is targeted by the exploit.
        If none it works it works for all.
    service: str
        The service which is targeted by the exploit.
        If none it works it works for all.
    acces: int
        The access level which is gained after succes.
    """

    def __init__(self,
                 name,
                 target,
                 cost,
                 duration,
                 prob=1.0,
                 req_access=AccessLevel.USER,
                 hardware=None,
                 os = None,
                 service=None,
                 access=0):

        super().__init__(name=name,
                         target=target,
                         cost=cost,
                         duration = duration,
                         prob=prob,
                         req_access=req_access)

        self.hardware = hardware
        self.os = os
        self.service = service
        self.access = access


class PrivilegeEscalation(Action):
    """
    PrivilegeEscalation  action and inherits base action from the Action Class.

    ...

    Attributes
    ----------
    os: str
        The operating system which is targeted by the exploit.
        If none it works it works for all.
    process : str
        The process which is targeted by the privilege escalation.
        If None the action works independent of a process.
    acces: int
        The access level which is gained after succes.
    """

    def __init__(self,
                 name,
                 target,
                 cost,
                 duration,
                 prob=1.0,
                 req_access=AccessLevel.USER,
                 os = None,
                 process= None,
                 access=0):

        super().__init__(name=name,
                         target=target,
                         cost=cost,
                         duration = duration,
                         prob=prob,
                         req_access=req_access)

        self.os = os
        self.process = process
        self.access = access

class SubnetScan(Action):
    """
    SubnetScan action and inherits base action from the Action Class.
    """

    def __init__(self,
                 duration,
                 cost,
                 prob=1.0,
                 req_access=AccessLevel.USER,
                 **kwargs):

        super().__init__("subnet_scan",
                         duration=duration,
                         cost=cost,
                         prob=prob,
                         req_access=req_access,
                         **kwargs)


class OSScan(Action):
    """
    OSScan action and inherits base action from the Action Class.
    """

    def __init__(self,
                 duration,
                 cost,
                 prob=1.0,
                 req_access=AccessLevel.USER,
                 **kwargs):

        super().__init__("os_scan",
                         duration=duration,
                         cost=cost,
                         prob=prob,
                         req_access=req_access,
                         **kwargs)

class HardwareScan(Action):
    """
    HardwareScan action and inherits base action from the Action Class.
    """

    def __init__(self,
                 duration,
                 cost,
                 prob=1.0,
                 req_access=AccessLevel.USER,
                 **kwargs):

        super().__init__("hardware_scan",
                         duration=duration,
                         cost=cost,
                         prob=prob,
                         req_access=req_access,
                         **kwargs)

class ServiceScan(Action):
    """
    ServiceScan action and inherits base action from the Action Class.
    """

    def __init__(self,
                 duration,
                 cost,
                 prob=1.0,
                 req_access=AccessLevel.USER,
                 **kwargs):

        super().__init__("service_scan",
                         duration=duration,
                         cost=cost,
                         prob=prob,
                         req_access=req_access,
                         **kwargs)

class ProcessScan(Action):
    """
    ProcessScan action and inherits base action from the Action Class.
    """

    def __init__(self,
                 duration,
                 cost,
                 prob=1.0,
                 req_access=AccessLevel.USER,
                 **kwargs):

        super().__init__("process_scan",
                         duration=duration,
                         cost=cost,
                         prob=prob,
                         req_access=req_access,
                         **kwargs)
