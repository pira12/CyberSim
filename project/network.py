import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
import globals as glob

from actions_def import Harden_host, Harden_edge
from actions_att import Exploit, PrivilegeEscalation
glob_atts_h = [PrivilegeEscalation("att_h1", 1, 10, 0.8, 1, process="p1"), PrivilegeEscalation("att_h2", 1, 10, 0.8, 1, process="p7")]
glob_atts_e = [Exploit("att_e1", 1, 10, 0.8, service="s1"), Exploit("att_e2", 1, 10, 0.8, service="s1")]

# glob_hard_h = [Harden_host("harden att_h1", 1, 10, "att_h1"), Harden_host("harden att_h2", 1, 10, "att_h2"), Harden_host("harden att_h3", 1, 10, "att_h3")]
# glob_hard_e = [Harden_edge("harden att_e1", 1, 10, "att_e1"), Harden_edge("harden att_e2", 1, 10, "att_e2"), Harden_edge("harden att_e3", 1, 10, "att_e3")]


class Host:
    """
    Class for the hosts.
    ----------
    subnet_addr : int
        The subnet address of the host.
    host_addr : int
        The host address of the host.
    score : int
        An indication how important the data of this host is.
    access_for_score : int
        The level of access the attacker needs to get to the data
        and thus get the amount of points that the data is worth.
    attacker_access_lvl : int
        The highest access level any of the attackers have
        in this host. This is the level the defender will see
        when it scans the host.
    priv_esc_hardened : [string]
        An array with all the privilege escalation attacks that this
        host is hardened against.
    hardware : string
        The hardware of the host. The host has only one hardware.
    processes : [string]
        The processes run on the host. This could be multiple.
    services : [string]
        The services run on the host. This could be multiple.
    os : string
        The operating system of the host.
    """
    def __init__(self, subnet_addr, host_addr, score, access_for_score,
                 attacker_access_lvl, priv_esc_hardened, hardware,
                 processes, services, os):

        self.subnet_addr = subnet_addr                  # int
        self.host_addr = host_addr                      # int
        self.score = score                              # int
        self.access_for_score = access_for_score        # int
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


    def get_score(self):
        """
        Return the score of the host.
        """
        return self.score


    def get_access_for_score(self):
        """
        Return the access needed to get the score of this host.
        """
        return self.access_for_score


    def get_attacker_access_lvl(self):
        """
        Return the  access level of the attacker.
        """
        return self.attacker_access_lvl


    def set_attacker_access_lvl(self, lvl):
        """
        Set the access level to the given level if it is higher.
        """
        if self.attacker_access_lvl < lvl:
            self.attacker_access_lvl = lvl


    def get_hardened(self):
        """
        Return the array of hardened attacks.
        """
        return self.priv_esc_hardened


    def get_hardware(self):
        """
        Return the hardware of the host.
        """
        return self.hardware


    def get_processes(self):
        """
        Return the processes of the host.
        """
        return self.processes


    def get_services(self):
        """
        Return the services of the host.
        """
        return self.services


    def get_os(self):
        """
        Return the os of the host.
        """
        return self.os


    def harden(self, attack_type):
        """
        Make it harder for attackers to use certain attacks on
        this host. The probability of succesfull with that attack will
        be lowered.
        ----------
        attack_type : string
        """
        if attack_type not in self.priv_esc_hardened:
            self.priv_esc_hardened.append(attack_type)


    def possible_attacks(self):
        """
        Return all the possible PrivilegeEscalations that work on this host.
        """
        poss_atts = []
        for att in glob_atts_h:
            if att.process in self.get_processes():
                poss_atts.append(att)

        return poss_atts

    def possible_attacks_names(self):
        """
        Return all the names of the possible PrivilegeEscalations
        that work on this host.
        """
        return [x.name for x in self.possible_attacks()]


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
        ----------
        attack_type : string
        """
        if attack_type not in self.exploits_hardened:
            self.exploits_hardened.append(attack_type)


    def get_both_addr(self):
        """
        Get both the source and destination address of the edge.
        """
        return (self.source_addr, self.dest_addr)


    def get_source_addr(self):
        """
        Get the source address of the edge.
        """
        return self.source_addr


    def get_dest_addr(self):
        """
        Get the destination address of the edge.
        """
        return self.dest_addr

    def get_hardened(self):
        """
        Return the array of hardened attacks.
        """
        return self.exploits_hardened


    def get_servs_allowed(self):
        """
        Return the services that are allowed on this edge.
        """
        return self.servs_allowed


    def possible_exploits(self):
        """
        Return all the possible PrivilegeEscalations that work on this host.
        """
        poss_exps = []
        for att in glob_atts_e:
            if att.service in self.get_servs_allowed():
                poss_exps.append(att)

        return poss_exps

    def possible_exploits_names(self):
        """
        Return all the names of the possible PrivilegeEscalations
        that work on this host.
        """
        return [x.name for x in self.possible_exploits()]


class Network:
    """
    Class for the Network
    The first host is the internet, from which the attacker starts
    ----------
    hosts : [Hosts]
        An array with all the hosts in the network.
    host_map : dictionary, key (int, int)
        A dictionary with as key (subnet addr, host addr).
        The returned data is the place in hosts of the host
        with the given address.
    edges : dictionary, key (int, int)
        A dictionary with as key (source numb, dest numb),
        these numbers can be found in host_map. The returned data
        is the edge between the hosts that are in the given positions
        in hosts.
    sensitive_hosts : [(int, int)]
        An array with all (subnet addr, host addr) of the hosts with
        sensitive information.
    failed_att_hosts : [(int, int)]
        An array with all (subnet addr, host addr) of the hosts that
        have been attack, but the attack failed.
    failed_att_edges : [((int, int), (int, int))]
        An array with all (source addr, destination addr) of the edges
        that have been attack, but the attack failed.
    adjacency_matrix : [[int]]
        The adjacency matrix of the network. There is an edge from
        host A to host B if adjacency_matrix[A number][B number] is 1.
        The numbers are the places in hosts. These can be retrieved with
        host_map.

    """

    def __init__(self):
        self.hosts = [Host(1, 0, 1, 0, 0, [], "Internet", [], [], "windows")]
        self.host_map = {(1, 0):0}      # The key is (subnet addr, host addr)
        self.edges = {}                 # The key is (source numb, dest numb)
        self.sensitive_hosts = []

        self.failed_att_hosts = []
        self.failed_att_edges = []

        self.adjacency_matrix = np.array([[0]])


    def add_host(self, host):
        """
        Add a node to the network.
        ----------
        host : Host
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
        ----------
        source_addr : (int, int)
        dest_addr : (int, int)
        servs_allowed : [string]
        """
        source = self.host_map[source_addr]
        dest = self.host_map[dest_addr]
        self.edges[(source, dest)] = Edge(source_addr, dest_addr, servs_allowed)

        self.adjacency_matrix[source][dest] = 1


    def add_sensitive_hosts(self, address):
        """
        Add a sensitive host to the network.
        The sensitive hosts are ordered from highest score
        to lowest score.
        ---------
        address : (int, int)
        """
        if address in self.host_map:
            self.sensitive_hosts.append(address)

            value = self.get_score_host(address)
            place = len(self.sensitive_hosts) - 2

            while place >= 0:
                if value <= self.get_score_host(self.sensitive_hosts[place]):
                    break

                temp = self.sensitive_hosts[place]
                self.sensitive_hosts[place] = self.sensitive_hosts[place + 1]
                self.sensitive_hosts[place + 1] = temp
                place -= 1

        else:
            print("The address", address, "is not in the network and can thus not be a sensitive host")


    def get_score_host(self, address):
        """
        Return the score of the host of the given address.
        """
        return self.get_host(address).get_score()


    def get_sensitive_hosts(self):
        """
        Get all addresses of the sensitive hosts of the network.
        """
        return self.sensitive_hosts


    def get_sensitive_hosts2(self):
        """
        Get all the sensitive hosts of the network.
        """
        return [self.get_host(x) for x in self.sensitive_hosts]


    def get_host_place(self, address):
        """
        Return the place of the host in hosts.
        ----------
        address : (int, int)
        """
        return self.host_map[address]


    def get_host(self, address):
        """
        Return the Host with the given address.
        ----------
        address : (int, int)
        """
        return self.hosts[self.get_host_place(address)]


    def get_edge(self, addresses):
        """
        Return the edge given addresses: ((source address), (destination address))
        ----------
        addresses : ((int, int), (int, int))
        """
        (source_address, destination_address) = addresses
        source_numb = self.get_host_place(source_address)
        dest_numb = self.get_host_place(destination_address)

        return self.edges[(source_numb, dest_numb)]


    def reachable_hosts(self, source_addr):
        """
        Return all the hosts that can be reached by the given host.
        ----------
        source_addr : (int, int)
        """
        source = self.get_host_place(source_addr)
        dests = []

        for i in range(0, len(self.adjacency_matrix)):
            if self.adjacency_matrix[source][i] == 1:
                dests.append(self.hosts[i])

        return dests


    def reach_this_host(self, dest_addr):
        """
        Return all the hosts that can reach the given host.
        ----------
        dest_addr : (int, int)
        """
        dest = self.get_host_place(dest_addr)
        sources = []

        for i in range(0, len(self.adjacency_matrix)):
            if self.adjacency_matrix[i][dest] == 1:
                sources.append(self.hosts[i])

        return sources


    def get_all_edges_from(self, source_addr):
        """
        Return all edges that start at the given host.
        ---------
        source_addr : (int, int)
        """
        source = self.get_host_place(source_addr)
        edges = []

        for i in range(0, len(self.adjacency_matrix)):
            if self.adjacency_matrix[source][i] == 1:
                edges.append(self.edges[(source, i)])

        return edges


    def get_all_edges_to(self, dest_addr):
        """
        Return all edges that go towards the given host.
        ----------
        dest_addr : (int, int)
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


    def get_all_hardened_hosts(self):
        """
        Return the place in the array hosts of all hosts that are
        hardened against some attack.
        """
        hardened_hosts = []

        for i in range(0, len(self.hosts)):
            if self.hosts[i].get_hardened() != []:
                hardened_hosts.append(i)

        return hardened_hosts


    def get_all_compromised_hosts(self):
        """
        Return the place in the array hosts of all hosts that are
        compromised.
        """
        compromised_host = []

        for i in range(0, len(self.hosts)):
            if self.hosts[i].get_attacker_access_lvl() != 0:
                compromised_host.append(i)

        return compromised_host


    def get_failed_att_hosts(self):
        """
        Get all the hosts that have been attacked, but the attack failed.
        """
        return self.failed_att_hosts


    def add_failed_att_hosts(self, host):
        """
        Add an failed attack on a host to the array of failed attacks
        on hosts.
        ----------
        host : Host
        """
        self.failed_att_hosts.append(host)


    def reset_failed_att_hosts(self):
        """
        Empty the array of failed attacks on hosts.
        """
        self.failed_att_hosts = []


    def get_failed_att_edges(self):
        """
        Get all the edges that have been attacked, but the attack failed.
        """
        return self.failed_att_edges


    def add_failed_att_edges(self, edge):
        """
        Add an failed attack on an edge to the array of failed attacks
        on edges.
        ----------
        edge : Edge
        """
        self.failed_att_edges.append(edge)


    def reset_failed_att_edges(self):
        """
        Get all the edges that have been attacked, but the attack failed.
        """
        self.failed_att_edges = []


def create_basic_network(numb1, numb2):
    """
    Creates a random graph and create a network based on the graph.
    Return the graph, the network and the positions.
    ----------
    numb1: int
        The number of hosts in the first subnet. At least 2.
    numb2: int
        The number of hosts in the second subnet. At least 2.
    """
    if numb1 < 2:
        numb1 = 2
    if numb2 < 2:
        numb2 = 2

    # G = nx.powerlaw_cluster_graph(numb1, 1, 0.4)
    # pos = nx.spring_layout(G, seed=3113794652)  # positions for all nodes

    N = Network()
    N.add_host(Host(2, 0, 100, 2, 0, [], glob.hardware[0], glob.processes[0:2], glob.services[0:2], glob.os[0]))
    N.add_host(Host(3, 0, 110, 2, 0, [], glob.hardware[0], glob.processes[0:2], glob.services[0:2], glob.os[0]))
    # N.add_host(Host(2, 0, 100, 2, 0, [], "Lenovo", ["p1", "p2"], ["s1", "s2"], "windows"))
    # N.add_host(Host(3, 0, 110, 2, 0, [], "Lenovo", ["p1", "p2"], ["s1", "s2"], "windows"))

    for numb in range(1, numb1):
        # N.add_host(Host(2, numb, 10, 2, 0, [], "Lenovo", ["p1", "p2"], ["s1", "s2"], "windows"))
        N.add_host(Host(2, numb, 10, 2, 0, [], glob.hardware[0], glob.processes[0:2], glob.services[0:2], glob.os[0]))

    for numb in range(1, numb2):
        # N.add_host(Host(3, numb, 10, 2, 0, [], "Lenovo", ["p1", "p2"], ["s1", "s2"], "windows"))
        N.add_host(Host(3, numb, 10, 2, 0, [], glob.hardware[0], glob.processes[0:2], glob.services[0:2], glob.os[0]))


    N.add_sensitive_hosts((2,0))
    N.add_sensitive_hosts((3,1))
    N.add_sensitive_hosts((3,0))


    for numb in range(1, numb1):
        N.add_edge((1, 0), (2, numb), glob.services[0:1])
        N.add_edge((2, 0), (2, numb), glob.services[0:1])
        N.add_edge((2, numb), (2, 0), glob.services[0:1])

    for numb in range(1, numb2):
        N.add_edge((3, 0), (3, numb), glob.services[0:1])
        N.add_edge((3, numb), (3, 0), glob.services[0:1])

    N.add_edge((2, 0), (3, 0), glob.services[0:1])

    return N


def draw_network(network):
    G = nx.DiGraph(network.adjacency_matrix)
    pos = nx.spring_layout(G, seed=3113794652)  # positions for all nodes

    nx.draw(G, pos, node_color="tab:orange")
    hardened_hosts = network.get_all_hardened_hosts()
    nx.draw(G, pos, nodelist=hardened_hosts, node_color="tab:blue")
    compromised_hosts = network.get_all_compromised_hosts()
    nx.draw(G, pos, nodelist=compromised_hosts, node_color="tab:red")

    # nx.draw(N.graph, pos, nodelist=N.public, node_color="tab:orange")
    # nx.draw(N.graph, pos, nodelist=N.non_public, node_color="tab:blue")
    # nx.draw(N.graph, pos, nodelist=N.compromised_nodes, node_color="tab:red")

    labels = {}
    for n in G.nodes:
        # labels[n] = n
        labels[n] = network.hosts[n].get_address()

    nx.draw_networkx_labels(G, pos, labels, font_size=8, font_color="whitesmoke")
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

    print(N.get_host((1,0)))
    print(N.get_edge(((1, 0), (2, 1))))


    # draw_network(N)
