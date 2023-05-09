# import simpy

"""
**Actions_def:**

Every action inherits from the base :class:`Action_def` class, which defines
some common attributes and functions. Different types of actions
are implemented as subclasses of the Action class.

Defender action types implemented:

- :class:`Harden_host`
- :class:`Harden_edge`


"""

class Action_def:
    """
    The base action classs for Defender actions.
    ...
    Attributes
    ----------
    name : str
        The name of action
    cost : float
        The cost of performing the action.
    duration : float
        The time it takes for the action to finish.
    prob : float
        The success probability of the action. This is the probability that
        the action works given that it's preconditions are met.
    env : Environment
        The environment in which the action is taking place.
    """

    def __init__(self,
                 name,
                 cost,
                 duration,
                 prob=1.0):

        self.name = name
        self.cost = cost
        self.duration = duration
        self.prob = prob



class Harden_host(Action_def):
    """
    Harden_host action and inherits base action from the Action_def Class.

    ...

    Attributes
    ----------
    attack_type: : string
        The attack type the edge will be prepared against.
    """

    def __init__(self,
                 name,
                 cost,
                 duration,
                 attack_type,
                 prob=1.0):

        super().__init__(name=name,
                         cost=cost,
                         duration=duration,
                         prob=prob)

        self.attack_type = attack_type

    def get_duration(self):
        """
        Return the duration of the hardening of the host.
        """
        return self.duration

    def get_attack_type(self):
        """
        Return the attack_type against which the host is being hardened.
        """
        return self.attack_type


    def get_cost(self):
        """
        Return the cost of the action.
        """
        return self.cost




class Harden_edge(Action_def):
    """
    Harden_edge action and inherits base action from the Action_def Class.

    ...

    Attributes
    ----------
    attack_type: : string
        The attack type the edge will be prepared against.
    target : Edge
        The target of the action is edge that the action is being used on.
    """

    def __init__(self,
                 name,
                 cost,
                 duration,
                 attack_type,
                 prob=1.0):

        super().__init__(name=name,
                         cost=cost,
                         duration=duration,
                         prob=prob)

        self.attack_type = attack_type


    def get_duration(self):
        """
        Return the duration of the hardening of the host
        """
        return self.duration

    def get_attack_type(self):
        """
        Return the attack_type against which the host is being hardened.
        """
        return self.attack_type


    def get_cost(self):
        """
        Return the cost of the action.
        """
        return self.cost


