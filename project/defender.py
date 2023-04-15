import random

class Defender:
    def __init__(self, strategy):
        self.strategy = strategy
        self.vulnerable_nodes = set()
        self.compromised_nodes = set()

    def defend_nodes(self, network):
        """Function to start defending node which was compromised."""
        for node in self.compromised_nodes:
            if(random.random() > 0.5):
                self.compromised_nodes.remove(node)
                network.compromised_nodes.remove(node.node_id)
                node.make_compromised()

    def mitigate_nodes(self, network):
        """Function to start defending node with vulnerability."""
        for node in network.nodes:
            if(random.random() > 0.5):
                node.patch()

    def scan_network(self, network):
        """ Function to scan the nodes in a network for vulnerabilities"""
        for node in network.nodes:
            # If node is public and vulnerable then add to viable nodes.
            if(node.vulnerable):
                self.vulnerable_nodes.add(node)
