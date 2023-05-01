import random
import simpy
from network import create_basic_network
from actions_def import Harden_host, Harden_edge

class Defender:
    def __init__(self, strategy, network, env):
        self.strategy = strategy
        self.network = network
        self.score = 0
        self.env = env

        self.host_attacks = ["att_h1"]
        self.edge_attacks = ["att_e1"]

        self.harden_h1 = Harden_host("harden att_h1", 1, 5, "att_h1", env)
        self.harden_e1 = Harden_edge("harden att_e1", 1, 5, "att_e1", env)


    def random_defense(self):
        """
        Add a defense to a random host or edge.
        """
        if random.random() >= 0.5:
            random_host = self.network.get_random_host()
            self.harden_h1.do_host_hardening(random_host)

        else:
            random_edge = self.network.get_random_edge()
            self.harden_e1.do_edge_hardening(random_edge)


envi = simpy.Environment()
net = create_basic_network(5, 3)
D = Defender("random", net, envi)
D.random_defense()

print(D.network.get_all_host_hardenings())
print(D.network.get_all_edge_hardenings())
