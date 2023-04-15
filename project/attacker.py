import random

class Attacker:
    def __init__(self, strategy):
        self.strategy = strategy
        self.viable_nodes = set()
        self.compromised_nodes = set()

    def attack_nodes(self, network):
        """Function to start attack on node with vulnerability."""
        for node in self.viable_nodes:
            if(random.random() > 0.5):
                self.compromised_nodes.add(node)
                network.compromised_nodes.append(node.node_id)

    def scan_network(self, network):
        """ Function to scan the public nodes in a network."""
        for node in network.nodes:
            # If node is public and vulnerable then add to viable nodes.
            if(node.node_id in network.public and node.vulnerable):
                self.viable_nodes.add(node)

