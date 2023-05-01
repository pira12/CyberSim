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
                 priv_esc_hardened, hardware, processes, services, os):

        self.subnet_addr = subnet_addr                  # int
        self.host_addr = host_addr                      # int
        self.score = score                              # int
        self.access_for_score = access_for_score        # int
        self.host_discovered = host_discovered          # bool
        self.host_reached = host_reached                # bool
        self.attacker_access_lvl = attacker_access_lvl  # int
        self.priv_esc_hardened = priv_esc_hardened      # [string]
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


    def harden(self, attack_type):
        """
        Make it harder for attackers to use certain attacks on
        this host. The probability of succesfull with that attack will
        be lowered.
        """
        if attack_type not in self.priv_esc_hardened:
            self.priv_esc_hardened.append(attack_type)


    def get_hardened(self):
        """
        Return the array of hardened attacks.
        """
        return self.priv_esc_hardened


# Host(sub, host, 10, 2, False, False, 0, [], "Lenovo", ["p1", "p2"], ["s1", "s2"], "windows")


class Edge:
    """
    Class for edges in the network
    """
    def __init__(self, source_addr, dest_addr, servs_allowed):
        self.source_addr = source_addr
        self.dest_addr = dest_addr
        self.exploits_hardened = []
        self.servs_allowed = servs_allowed

    def harden(self, attack_type):
        """
        Make it harder for attackers to use certain attacks on
        this edge. The probability of succesfull with that attack will
        be lowered.
        """
        if attack_type not in self.exploits_hardened:
            self.exploits_hardened.append(attack_type)


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

    def get_hardened(self):
        """
        Return the array of hardened attacks.
        """
        return self.exploits_hardened


class Network:
    """
    Class for the Network
    The first host is the internet, from which the attacker starts
    """

    def __init__(self):
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

        self.adjacency_matrix[source][dest] = 1

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
            if self.adjacency_matrix[source][i] == 1:
                dests.append(self.hosts[i])

        return dests


    def reach_this_host(self, dest_addr):
        """
        Return all the hosts that can reach the given host
        """
        dest = self.get_host_place(dest_addr)
        sources = []

        for i in range(0, len(self.adjacency_matrix)):
            if self.adjacency_matrix[i][dest] == 1:
                sources.append(self.hosts[i])

        return sources


    def get_all_edges_from(self, source_addr):
        """
        Return all edges that start at the given host
        """
        source = self.get_host_place(source_addr)
        edges = []

        for i in range(0, len(self.adjacency_matrix)):
            if self.adjacency_matrix[source][i] == 1:
                edges.append(self.edges[(source, i)])

        return edges


    def get_all_edges_to(self, dest_addr):
        """
        Return all edges that go towards the given host
        """
        dest = self.get_host_place(dest_addr)
        edges = []

        for i in range(0, len(self.adjacency_matrix)):
            if self.adjacency_matrix[i][dest] == 1:
                edges.append(self.edges[(i, dest)])

        return edges


    def get_random_host(self):
        """
        Return a random hosts from the network and 1 otherwise.
        This does not include the first host, because the first
        host symbolises the interner from which the attacker starts
        and in not truly part of the IT structure of the company.
        """

        if len(self.hosts) == 1:
            print("Cannot get a random host because there is noone")
            return 1

        random_numb = random.randint(1, len(self.hosts)-1)
        return self.hosts[random_numb]

    def get_random_edge(self):
        """
        Return a random edge from the network and 1 otherwise.
        """
        if np.sum(self.adjacency_matrix) == 0:
            print("Cannot get a random edge because there is noone")
            return 1

        while(1):
            random_numb1 = random.randint(0, len(self.hosts)-1)
            random_numb2 = random.randint(0, len(self.hosts)-1)

            if self.adjacency_matrix[random_numb1][random_numb2] == 1:
                return self.edges[(random_numb1, random_numb2)]


    def get_all_host_hardenings(self):
        """
        Return all the attack types each host is hardened against.
        """
        return [h.get_hardened() for h in self.hosts]


    def get_all_edge_hardenings(self):
        """
        Return all the attack types each host is hardened against.
        """
        return [e.get_hardened() for e in self.edges.values()]






def create_basic_network(numb1, numb2):
    """
    Creates a random graph and create a network based on the graph.
    Return the graph, the network and the positions.
    """

    # G = nx.powerlaw_cluster_graph(numb1, 1, 0.4)
    # pos = nx.spring_layout(G, seed=3113794652)  # positions for all nodes

    N = Network()

    for numb in range(0, numb1):
        N.add_host(Host(2, numb, 10, 2, False, False, 0, [], "Lenovo", ["p1", "p2"], ["s1", "s2"], "windows"))

    for numb in range(0, numb2):
        N.add_host(Host(3, numb, 10, 2, False, False, 0, [], "Lenovo", ["p1", "p2"], ["s1", "s2"], "windows"))


    N.add_sensitive_hosts((2,0))
    N.add_sensitive_hosts((3,0))


    for numb in range(1, numb1):
        N.add_edge((1, 0), (2, numb), ["s1"])
        N.add_edge((2, 0), (2, numb), ["s1"])
        N.add_edge((2, numb), (2, 0), ["s1"])

    for numb in range(1, numb2):
        N.add_edge((3, 0), (3, numb), ["s1"])
        N.add_edge((3, numb), (3, 0), ["s1"])

    N.add_edge((2, 0), (3, 0), ["s1"])


    return N

def draw_network(network):
    G = nx.DiGraph(network.adjacency_matrix)
    pos = nx.spring_layout(G, seed=3113794652)  # positions for all nodes

    nx.draw(G, pos, node_color="tab:orange")

    # nx.draw(N.graph, pos, nodelist=N.public, node_color="tab:orange")
    # nx.draw(N.graph, pos, nodelist=N.non_public, node_color="tab:blue")
    # nx.draw(N.graph, pos, nodelist=N.compromised_nodes, node_color="tab:red")

    labels = {}
    for n in G.nodes:
        labels[n] = n

    nx.draw_networkx_labels(G, pos, labels, font_size=11, font_color="whitesmoke")
    plt.show()

if __name__ == '__main__':
    N = create_basic_network(5, 3)

    print(N.get_host_place((2,0)))
    print(N.adjacency_matrix)
    print(N.edges[(0, 2)].servs_allowed)

    print([x.source_addr for x in N.get_all_edges_to((2, 0))])
    print([x.source_addr for x in N.get_all_edges_from((2, 0))])

    print([x.get_address() for x in N.reach_this_host((2, 0))])
    print([x.get_address() for x in N.reachable_hosts((2, 0))])

    print(N.get_random_edge())
    print(N.get_random_host())


    draw_network(N)
