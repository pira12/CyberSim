import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np



# print(nx.info(G))
# print([e for e in G.edges])
# print(G.degree(0))


class Host:
    """
    Class for the nodes
    """
    def __init__(self, subnet_addr, host_addr, score, access_for_score,
                 host_discovered, host_reached, attacker_access_lvl,
                 priv_esc_hardend, hardware, processes, services, os):

        self.subnet_addr = subnet_addr                  # int
        self.host_addr = host_addr                      # int
        self.score = score                              # int
        self.access_for_score = access_for_score        # int
        self.host_discovered = host_discovered          # bool
        self.host_reached = host_reached                # bool
        self.attacker_access_lvl = attacker_access_lvl  # int
        self.priv_esc_hardend = priv_esc_hardend        # [string]
        self.hardware = hardware                        # string
        self.processes = processes                      # [string]
        self.services = services                        # [string]
        self.os = os                                    # string


    def get_address(self):
        """
        Return the complete address of the host
        (subnet address, host address)
        """
        return (self.subnet_addr, self.host_addr)


# Host(sub, host, 10, 2, False, False, 0, [], "Lenovo", ["p1", "p2"], ["s1", "s2"], "windows")


class Edge:
    """
    Class for edges in the network
    """
    def __init__(self, source_addr, dest_addr, servs_allowed):
        self.source_addr = source_addr
        self.dest_addr = dest_addr
        self.exploits_hardend = []
        self.servs_allowed = servs_allowed

    def harden(self, exploit):
        """
        Make it harder for attackers to use certain exploits on
        this edge. The probability of succesfull with that exploit will
        be lowered.
        """
        self.exploits_hardend.append(exploit)


    def get_source_addr(self):
        """
        Get the source address of the edge
        """
        return self.source_addr


    def get_dest_addr(self):
        """
        Get the destination address of the edge
        """
        return self.dest_addr


class Network:
    """
    Class for the Network
    The first host is the internet, from which the attacker starts
    """
    # Do we still need graph? I changed egdges to a dict.
    def __init__(self, graph):
        self.graph = graph
        self.hosts = [Host(1, 0, 1, 0, False, False, 0, [], "Internet", [], [], "windows")]
        self.host_map = {(1, 0):0}      # The key is (subnet addr, host addr)
        self.edges = {}                 # The key is (source numb, dest numb) which can be found in host_map
        self.sensitive_hosts = []

        self.adjacency_matrix = np.array([[0]])


    def add_host(self, host):
        """
        Add a node to the network
        """
        self.hosts.append(host)
        addr = host.get_address()
        # Host_numb is the number the host has in the array self.hosts
        host_numb = len(self.host_map)
        self.host_map[addr] = host_numb

        self.adjacency_matrix = np.r_[self.adjacency_matrix, [np.zeros(host_numb)]]
        self.adjacency_matrix = np.c_[self.adjacency_matrix, np.zeros(host_numb + 1)]


# What to do when the edge already exists?
    def add_edge(self, source_addr, dest_addr, servs_allowed):
        """
        Add an edge tot the network.
        The column number is the source and the row number the destination
        in the adjacency matrix.
        """
        source = self.host_map[source_addr]
        dest = self.host_map[dest_addr]
        self.edges[(source, dest)] = Edge(source_addr, dest_addr, servs_allowed)

        self.adjacency_matrix[dest][source] = 1

    def add_sensitive_hosts(self, addr):
        """
        Add a sensitive host to the network
        """
        if addr in self.host_map:
            self.sensitive_hosts.append(addr)
        else:
            print("The address", addr, "is not in the network and can thus not be a sensitive host")


    def get_host_place(self, address):
        """
        Return the place of the host in hosts
        """
        return self.host_map[address]


    def reachable_hosts(self, source_addr):
        """
        Return all the hosts that can be reached by the given host
        """
        source = self.get_host_place(source_addr)
        dests = []

        for i in range(0, len(self.adjacency_matrix)):
            if self.adjacency_matrix[i][source] == 1:
                dests.append(self.hosts[i])

        return dests


    def reached_by_hosts(self, dest_addr):
        """
        Return all the hosts that can reach the given host
        """
        dest = self.get_host_place(dest_addr)
        sources = []

        for i in range(0, len(self.adjacency_matrix)):
            if self.adjacency_matrix[dest][i] == 1:
                sources.append(self.hosts[i])

        return sources


    def get_all_edges_from(self, source_addr):
        """
        Return all edges that start at the given host
        """
        source = self.get_host_place(source_addr)
        edges = []

        for i in range(0, len(self.adjacency_matrix)):
            if self.adjacency_matrix[i][source] == 1:
                edges.append(self.edges[(source, i)])

        return edges


    def get_all_edges_to(self, dest_addr):
        """
        Return all edges that go towards the given host
        """
        dest = self.get_host_place(dest_addr)
        edges = []

        for i in range(0, len(self.adjacency_matrix)):
            if self.adjacency_matrix[dest][i] == 1:
                edges.append(self.edges[(i, dest)])

        return edges




def create_network(number_of_hosts):
    """
    Creates a random graph and create a network based on the graph.
    Return the graph, the network and the positions.
    """

    G = nx.powerlaw_cluster_graph(number_of_hosts, 1, 0.4)
    pos = nx.spring_layout(G, seed=3113794652)  # positions for all nodes

    N = Network(G)

    for numb in range(0, number_of_hosts):
        N.add_host(Host(2, numb, 10, 2, False, False, 0, [], "Lenovo", ["p1", "p2"], ["s1", "s2"], "windows"))

    for numb in range(0, 3):
        N.add_host(Host(3, numb, 10, 2, False, False, 0, [], "Lenovo", ["p1", "p2"], ["s1", "s2"], "windows"))

    return N, pos


N, pos = create_network(20)

print(N.hosts[0].services)
print(N.hosts[0].get_address())
print(N.hosts[14].get_address())

print(N.get_host_place((2,0)))
N.add_sensitive_hosts((2,0))
N.add_sensitive_hosts((3,0))

N.add_edge((1, 0), (2,0), ["s1"])
print(N.adjacency_matrix)
print(N.edges[(0, 1)].servs_allowed)

print(N.reachable_hosts((1, 0)))
print(N.reached_by_hosts((2, 0)))
print(N.get_all_edges_from((1, 0)))
print(N.get_all_edges_to((2, 0)))



# def draw_network():
#     nx.draw(N.graph, pos, nodelist=N.public, node_color="tab:orange")
#     nx.draw(N.graph, pos, nodelist=N.non_public, node_color="tab:blue")
#     nx.draw(N.graph, pos, nodelist=N.compromised_nodes, node_color="tab:red")

#     labels = {}
#     for n in N.graph.nodes:
#         labels[n] = n

#     nx.draw_networkx_labels(N.graph, pos, labels, font_size=11, font_color="whitesmoke")
#     plt.show()