import random
from network import create_basic_network

class Defender:
    def __init__(self, strategy, network):
        self.strategy = strategy
        self.network = network
        self.score = 0

        self.host_attacks = ["att_h1"]
        self.edge_attacks = ["att_e1"]


    def harden_host(self, host, attack_type):
        """
        Harden a host against a certain type of attack.
        """
        host.harden(attack_type)


    def harden_edge(self, edge, attack_type):
        """
        Harden a host against a certain type of attack.
        """
        edge.harden(attack_type)


    def random_defense(self):
        """
        Add a defense to a random host or edge.
        """
        if random.random() >= 0.5:
            random_host = self.network.get_random_host()
            self.harden_host(random_host, self.host_attacks[0])

        else:
            random_edge = self.network.get_random_edge()
            self.harden_edge(random_edge, self.edge_attacks[0])


net = create_basic_network(5, 3)
D = Defender("random", net)
D.random_defense()

print(D.network.get_all_host_hardenings())
# test voor edges
