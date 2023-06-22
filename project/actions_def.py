# import simpy

"""
**Actions_def:**

Every defensive action inherits from the base :class:`Action_def` class,
which defines some common attributes and functions. Different types of
actions are implemented as subclasses of the Action class.

Defender action types implemented:

- :class:`Harden_host`
- :class:`Harden_edge`


"""

class Action_def:
    """
    The base action classs for Defender actions.
    ----------
    name : str
        The name of action
    cost : float
        The cost of performing the action.
    duration : float
        The time it takes for the action to finish.
    """
    def __init__(self,
                 name,
                 cost,
                 duration):

        self.name = name
        self.cost = cost
        self.duration = duration

    def get_cost(self):
        """
        Return the cost of the action.
        """
        return self.cost


    def get_duration(self):
        """
        Return the duration of the action.
        """
        return self.duration


class Harden_host(Action_def):
    """
    The Class for the action harden host.
    ----------
    attack_type: string
        The attack type the edge will be prepared against.
    """
    def __init__(self,
                 name,
                 cost,
                 duration,
                 attack_type):

        super().__init__(name=name,
                         cost=cost,
                         duration=duration)

        self.attack_type = attack_type

    def get_attack_type(self):
        """
        Return the attack_type against which the host is being hardened.
        """
        return self.attack_type


class Harden_edge(Action_def):
    """
    The Class for the action harden edge.
    ----------
    attack_type: string
        The attack type the edge will be prepared against.
    target: Edge
        The target of the action is edge that the action is being used on.
    """
    def __init__(self,
                 name,
                 cost,
                 duration,
                 attack_type):

        super().__init__(name=name,
                         cost=cost,
                         duration=duration)

        self.attack_type = attack_type


    def get_attack_type(self):
        """
        Return the attack_type against which the host is being hardened.
        """
        return self.attack_type


class Scan_host(Action_def):
    """
    The Class for the action scan host.
    The scanning action is never used in any strategy, thus
    this class is never used.
    """
    def __init__(self,
                 name,
                 cost,
                 duration):

        super().__init__(name=name,
                         cost=cost,
                         duration=duration)


class Update_host(Action_def):
    """
    The Class for the action update host.
    The update host action is never used in any strategy, thus
    this class is never used.
    ----------
    new_processes: [string]
        The processes that run on the host after the update.
    """
    def __init__(self,
                 name,
                 cost,
                 duration,
                 new_processes):

        super().__init__(name=name,
                         cost=cost,
                         duration=duration)

        self.new_processes = new_processes


    def get_new_processes(self):
        """
        Return the processes that run on the host after the update.
        """
        return self.new_processes



class Update_firewall(Action_def):
    """
    The Class for the action update firewall.
    The update firewall action is never used in any strategy, thus
    this class is never used.
    ----------
    new_services: [string]
        The services that are allowed by the firewall after the update.
    """
    def __init__(self,
                 name,
                 cost,
                 duration,
                 new_services):

        super().__init__(name=name,
                         cost=cost,
                         duration=duration)

        self.new_services = new_services


    def get_new_services(self):
        """
        Return the services that are allowed by the firewall after the update.
        """
        return self.new_services
