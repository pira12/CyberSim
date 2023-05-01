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
                 env,
                 prob=1.0):

        self.name = name
        self.cost = cost
        self.duration = duration
        self.env = env
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
                 env,
                 prob=1.0):

        super().__init__(name=name,
                         cost=cost,
                         duration=duration,
                         env=env,
                         prob=prob)

        self.attack_type = attack_type


    def do_host_hardening(self, target_host):
        """
        Harden a host against a certain type of attack.
        target_host : Host
            The target of the action is host that the action is being used on.
        """
        print("RRR")
        # yield self.env.timeout(self.cost)
        print("TTT")
        target_host.harden(self.attack_type)




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
                 env,
                 prob=1.0):

        super().__init__(name=name,
                         cost=cost,
                         duration=duration,
                         env=env,
                         prob=prob)

        self.attack_type = attack_type


    def do_edge_hardening(self, target_edge):
        """
        Harden a edge against a certain type of attack.
        target_edge : Edge
            The target of the action is edge that the action is being used on.
        """
        target_edge.harden(self.attack_type)
