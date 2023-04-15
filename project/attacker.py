from multiprocessing import Process
import time

class Attacker:
    def __init__(self, strategy):
        self.strategy = strategy
        self.hacked_nodes = []

    # def attack_node(self, node):
    #     """Function to start attack on node with vulnerability."""
    #     time.sleep(5)
    #     self.hacked_nodes.append(node)

    def scan_network(self, public_nodes):
        """ Function to scan the public nodes in a network."""
        for node in public_nodes:
            # If public node is vulnerable, then attack else continue.
            if(node.vulnerable):
                
