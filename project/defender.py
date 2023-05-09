import random
import simpy
from actions_def import Harden_host, Harden_edge
import globals as glob

class Defender:
    def __init__(self, env, network, strategy):
        self.env = env
        self.network = network
        self.strategy = strategy
        self.score = 0

        self.host_attacks = ["att_h1"]
        self.edge_attacks = ["att_e1"]

        self.harden_h1 = Harden_host("harden att_h1", 1, 10, "att_h1")
        self.harden_e1 = Harden_edge("harden att_e1", 1, 10, "att_e1")


    def subtract_score(self, numb):
        """
        Subtract a number from the score.
        """
        self.score -= numb


    def run(self):
        """
        The main process, which the attacker repeats until the simulation is terminated.
        """
        # Load attacks to launch based on attack strategy
        # self.load_actions()

        while True:
            if self.strategy == "random":
                yield self.env.process(self.random_defense())


    def random_defense(self):
        """
        Add a defense to a random host or edge.
        """
        if random.random() >= 0.5:
            random_host = self.network.get_random_host()
            yield self.env.process(self.harden_host(random_host, self.harden_h1))

        else:
            random_edge = self.network.get_random_edge()
            yield self.env.process(self.harden_edge(random_edge, self.harden_e1))


    def harden_host(self, target_host, harden_action):
        """
        Harden a host against a certain type of attack.
        target_host : Host
        """
        glob.logger.info(f"Start Harden_host at {self.env.now} on host {target_host.get_address()}.")
        yield self.env.timeout(harden_action.get_duration())
        target_host.harden(harden_action.get_attack_type())
        self.subtract_score(harden_action.get_cost())
        print(self.score)
        glob.logger.info(f"Host {target_host.get_address()} hardened against {harden_action.get_attack_type()} at {self.env.now}.")


    def harden_edge(self, target_edge, harden_action):
        """
        Harden an edge against a certain type of attack.
        target_edge : Edge
        """
        glob.logger.info(f"Start Harden_edge at {self.env.now} on edge {target_edge.get_both_addr()}.")
        yield self.env.timeout(harden_action.get_duration())
        target_edge.harden(harden_action.get_attack_type())
        self.subtract_score(harden_action.get_cost())
        glob.logger.info(f"Edge {target_edge.get_both_addr()} hardened against {harden_action.get_attack_type()} at {self.env.now}.")
