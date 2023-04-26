import random
from globals import AttackStrat

class Attacker:
    """
    This is the class for the attacker.
    ...
    Attributes
    ----------
    env : Simpy Enviroment
        The Simpy enviroment of the simulator.
    network : Network
        The Netork with all the hosts and edges.
    process : Process
        The process of the attacker running.
    strategy : int
        The strategy chosen for the attacker
    compromised hosts : [hosts]
        The list with hosts which have been compromised by this attacker.
    score : AccessLevel,
        The won score by compromising the network for this attacker.
    """

    def __init__(self, env, network, strategy):
        self.env = env
        self.network = network
        self.process = env.process(self.run())
        self.strategy = strategy
        self.compromised_hosts = []
        self.score = 0


    def run(self):
        while True:
            # Choose attack to launch based on attack strategy
            attack_type = self.choose_attack()

            # Launch the chosen attack
            attack_start = self.env.now()
            # TODO! : Run the attack host
            # TODO! : Log the attack

            # Wait for the attack to finish
            yield self.env.timeout(10) # For now set to 10, but varies

            # If the attack succeeded increase score and Log it.
            if random.random() < self.attack_strategy[attack_type]:
                self.score += 1


    def choose_attack(self):
        """
        Choose attack based on attack strategy and compromised hosts.
        """
        if self.attack_strategy == AttackStrat.RAND:
            
        if self.attack_strategy == AttackStrat.AGRO:
            None
        if self.attack_strategy == AttackStrat.DEFF:
            None
