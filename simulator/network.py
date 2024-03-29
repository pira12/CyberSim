import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
import globals as glob
from matplotlib.lines import Line2D


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
        This property is not used.
    attacker_access_lvl : int
        The highest access level any of the attackers have
        in this host. This is the level the defender will see
        when it scans the host.
    priv_esc_hardened : [string]
        An array with all the privilege escalation attacks that this
        host is hardened against.
    hardware : string
        The hardware of the host. The host has only one hardware.
        This property is not used.
    processes : [string]
        The processes run on the host. This could be multiple.
    services : [string]
        The services run on the host. This could be multiple.
        This property is not used.
    os : string
        The operating system of the host.
        This property is not used.
    """
    def __init__(self, subnet_addr, host_addr, score, access_for_score,
                 attacker_access_lvl, priv_esc_hardened, hardware,
                 processes, services, os):

        self.subnet_addr = subnet_addr                  # int
        self.host_addr = host_addr                      # int
        self.score = score                              # int
        self.access_for_score = access_for_score        # int,      not used
        self.attacker_access_lvl = attacker_access_lvl  # int
        self.priv_esc_hardened = priv_esc_hardened      # [string]
        self.hardware = hardware                        # string,   not used
        self.processes = processes                      # [string]
        self.services = services                        # [string], not used
        self.os = os                                    # string,   not used


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


    def change_score(self, new_score):
        """
        Return the score of the host.
        """
        self.score = new_score


    def get_access_for_score(self):
        """
        Return the access needed to get the score of this host.
        This function is not used, since access_for_score is not used.
        """
        return self.access_for_score


    def get_attacker_access_lvl(self):
        """
        Return the access level of the attacker.
        """
        return self.attacker_access_lvl


    def set_attacker_access_lvl(self, lvl):
        """
        Set the access level to the given level if it is higher.
        The lvl cannot be higher than the root access.
        """
        if self.attacker_access_lvl < lvl and self.attacker_access_lvl <= glob.AccessLevel.ROOT:
            self.attacker_access_lvl = lvl


    def get_hardened(self):
        """
        Return the array of hardened attacks.
        """
        return self.priv_esc_hardened


    def get_hardware(self):
        """
        Return the hardware of the host.
        This function is not used, since the hardware is not used.
        """
        return self.hardware


    def get_processes(self):
        """
        Return the processes of the host.
        """
        return self.processes


    def update_processes(self, new_processes):
        """
        Change the processes of the host.
        The update host action is never used in any strategy, thus
        this function is only used in a function that is never used.
        ----------
        new_processes: [string]
        """
        self.processes = new_processes


    def get_services(self):
        """
        Return the services of the host.
        This function is not used, since the services of the host are not used.
        """
        return self.services


    def get_os(self):
        """
        Return the os of the host.
        This function is not used, since the os is not used.
        """
        return self.os


    def harden(self, attack_type):
        """
        Make it harder for attackers to use certain attacks on
        this host. The probability of succesfull with that attack will
        be lowered.
        ----------
        attack_type: string
        """
        if attack_type not in self.priv_esc_hardened:
            self.priv_esc_hardened.append(attack_type)


    def possible_attacks(self):
        """
        Return all the possible Privilege Escalations that work on this host.
        """
        poss_atts = []
        for att in glob.atts_h:
            if att.get_process() in self.get_processes():
                if att.get_name() not in self.get_hardened():
                    poss_atts.append(att)

        return poss_atts

    def possible_attacks_names(self):
        """
        Return all the names of the possible Privilege Escalations
        that work on this host.
        """
        return [x.get_name() for x in self.possible_attacks()]


class Edge:
    """
    Class for edges in the network
    ----------
    source_addr: (int, int)
        The address of the host that the edge is coming from.
    dest_addr: (int, int)
        The address of the host that the edge is going to.
    exploits_hardened: [string]
        The exploits that do not work anymore on this edge.
    servs_allowed: [string]
        The services that the destination host accepts via this edge.
    """
    def __init__(self, source_addr, dest_addr, servs_allowed):
        self.source_addr = source_addr
        self.dest_addr = dest_addr
        self.exploits_hardened = []
        self.servs_allowed = servs_allowed

    def harden(self, attack_type):
        """
        Prevent the attackers from using the attack_type on
        this edge. The attackers will fail if they use an attack
        which this edge is hardened against.
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
        These are the services that are not blocked by the firewall.
        """
        return self.servs_allowed


    def update_servs_allowed(self, new_servs):
        """
        Change the services that are allowed on this edge.
        The update firewall action is never used in any strategy, thus
        this function is only used in a function that is never used.
        ----------
        new_servs: [string]
        """
        self.servs_allowed = new_servs


    def possible_exploits(self):
        """
        Return all the possible exploits that work on this edge.
        """
        poss_exps = []
        for att in glob.atts_e:
            if att.get_service() in self.get_servs_allowed():
                if att.get_name() not in self.get_hardened():
                    poss_exps.append(att)


        return poss_exps

    def possible_exploits_names(self):
        """
        Return all the names of the possible exploits
        that work on this edge.
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
        self.hosts = [Host(1, 0, 0, 0, 2, [], "Internet", [], [], "windows")]
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


    def delete_host(self, address):
        """
        Add a node to the network.
        ----------
        address : (source address, destination address)
        """

        place = self.get_host_place(address)
        del self.hosts[place]
        del self.host_map[address]

        for key in self.host_map.keys():
            if self.host_map[key] > place:
                self.host_map[key] -= 1

        new_edges = {}

        # Make a new dictionary for the edges, since the places
        # of the hosts are changed by deleting one host.
        for (source, dest) in self.edges.keys():
            if source == place or dest == place:
                continue

            if source > place:
                new_source = source - 1
            else:
                new_source = source

            if dest > place:
                new_dest = dest - 1
            else:
                new_dest = dest

            new_edges[(new_source, new_dest)] = self.edges[(source, dest)]

        self.edges = new_edges

        self.adjacency_matrix = np.delete(self.adjacency_matrix,(place), axis=0)
        self.adjacency_matrix = np.delete(self.adjacency_matrix,(place), axis=1)



    def add_edge(self, source_addr, dest_addr, servs_allowed):
        """
        Add an edge to the network.
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


    def delete_edge(self, source_addr, dest_addr):
        """
        Delete an edge from the network.
        The column number is the source and the row number the destination
        in the adjacency matrix.
        ----------
        source_addr : (int, int)
        dest_addr : (int, int)
        """
        source = self.host_map[source_addr]
        dest = self.host_map[dest_addr]
        del self.edges[(source, dest)]

        self.adjacency_matrix[source][dest] = 0


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


    def delete_sensitive_hosts(self, address):
        """
        Delete a sensitive host from the network.
        ---------
        address : (int, int)
        """
        self.sensitive_hosts.remove(address)


    def get_score_host(self, address):
        """
        Return the score of the host of the given address.
        """
        return self.get_host(address).get_score()


    def get_sensitive_hosts(self):
        """
        Get allthe  addresses of the sensitive hosts of the network.
        """
        return self.sensitive_hosts


    def get_sensitive_hosts2(self):
        """
        Get all the sensitive hosts of the network.
        """
        return [self.get_host(x) for x in self.sensitive_hosts]


    def get_number_of_hosts(self):
        """
        Return the number of hosts in the network.
        """
        return len(self.hosts)


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


    def get_host_given_place(self, place):
        """
        Return the Host at the given place in hosts
        ----------
        place : int
        """
        return self.hosts[place]


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


    def get_edge_given_places(self, u, v):
        """
        Return the edge given the places of the hosts the edge connects.
        ----------
        u : int
            Place of the source host.
        v : int
            Place of the destination host.
        """
        address_source = self.get_host_given_place(u).get_address()
        address_destination = self.get_host_given_place(v).get_address()
        return self.get_edge((address_source, address_destination))


    def check_edge_addr(self, source_address, destination_address):
        """
        Check if an edge exists.
        ----------
        source_address : (int, int)
            Place of the source host.
        destination_address : (int, int)
            Place of the destination host.
        """
        source_numb = self.get_host_place(source_address)
        dest_numb = self.get_host_place(destination_address)
        return self.adjacency_matrix[source_numb][dest_numb]



    def check_edge(self, u, v):
        """
        Check if an edge exists.
        ----------
        u : int
            Place of the source host.
        v : int
            Place of the destination host.
        """
        return self.adjacency_matrix[u][v]


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


    def get_most_connected_neighbour(self, host_numb):
        """
        Get the neighbour of the given host that has the most edges.
        All hosts that have an edge to or from the given host are considered
        a neighbour. A random host among the best will be picked when there
        are multiple hosts with the most edges.
        """
        all_neighbours = []

        # Find all neighbours.
        for i in range(0, len(self.adjacency_matrix)):
            if self.adjacency_matrix[i][host_numb] == 1:
                all_neighbours.append(i)
            elif self.adjacency_matrix[host_numb][i] == 1:
                all_neighbours.append(i)

        best = 0
        best_edges = 0

        # Find the neighbour with the most edges.
        for n in all_neighbours:
            edges_out = np.sum(self.adjacency_matrix[n])
            edges_in = np.sum(self.adjacency_matrix[:, n])
            total_edges = edges_out + edges_in

            if total_edges > best_edges:
                best = n
                best_edges = total_edges
            elif total_edges == best_edges:
                if random.randint(0, 1):
                    best = n

        return best


    def get_most_connected_host(self):
        """
        Get the host that has the most edges.
        """
        best = 0

        for host_numb in range(len(self.hosts)) :
            all_neighbours = []

            # Find all neighbours.
            for i in range(0, len(self.adjacency_matrix)):
                if self.adjacency_matrix[i][host_numb] == 1:
                    all_neighbours.append(i)
                elif self.adjacency_matrix[host_numb][i] == 1:
                    all_neighbours.append(i)

            best = 0
            best_edges = 0

            # Find the neighbour with the most edges.
            for n in all_neighbours:
                edges_out = np.sum(self.adjacency_matrix[n])
                edges_in = np.sum(self.adjacency_matrix[:, n])
                total_edges = edges_out + edges_in

                if total_edges > best_edges:
                    best = n
                    best_edges = total_edges
                elif total_edges == best_edges:
                    if random.randint(0, 1):
                        best = n

        return best


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
        compromised. We distinguish between the different levels
        at which the hosts can be compromised.
        """
        compromised_host_lvl1 = []
        compromised_host_lvl2 = []

        for i in range(0, len(self.hosts)):
            if self.hosts[i].get_attacker_access_lvl() == 1:
                compromised_host_lvl1.append(i)
            elif self.hosts[i].get_attacker_access_lvl() >= 2:
                compromised_host_lvl2.append(i)

        return compromised_host_lvl1, compromised_host_lvl2


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
        self.failed_att_hosts.append(host.get_address())


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
        self.failed_att_edges.append(edge.get_both_addr())


    def reset_failed_att_edges(self):
        """
        Get all the edges that have been attacked, but the attack failed.
        """
        self.failed_att_edges = []


    def calculate_score(self):
        """
        Return the total score in the network and the sum of the
        hosts that are compromised by an attacker.
        """
        total = 0
        comprimised_score = 0
        for host in self.hosts:
            if host.get_attacker_access_lvl() > 1:
                comprimised_score += host.get_score()

            total += host.get_score()

        return total, comprimised_score


    def draw_pre_attack_network(self):
        G = nx.DiGraph(self.adjacency_matrix)
        pos = nx.spring_layout(G, seed=3113794652)  # positions for all nodes

        plt.figure()

        # Create the legend.
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', label='Network',markerfacecolor='tab:orange', markersize=10),
            Line2D([0], [0], marker='o', color='w', label='Internet',markerfacecolor='maroon', markersize=10),
        ]
        plt.legend(handles=legend_elements, loc='best')

        # Draw the normal and hardened hosts.
        nx.draw(G, pos, node_color="tab:orange")


        # Draw the internet.
        _, internet = self.get_all_compromised_hosts()
        nx.draw(G, pos, nodelist=internet, node_color="maroon")

        labels = {}
        for n in G.nodes:
            add1, add2 = self.hosts[n].get_address()
            labels[n] = str(add1) + ", " + str(add2)

        nx.draw_networkx_labels(G, pos, labels, font_size=6, font_color="whitesmoke")
        # plt.show()
        plt.savefig(f"./created_network.png", format="PNG")
        plt.close()



def create_basic_network(numb1, numb2):
    """
    Creates a basic network.
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

    N = Network()

    # Add the hosts to the network.
    N.add_host(Host(2, 0, 100, 2, 0, [], glob.hardware[0], glob.processes[0:2], glob.services[0:2], glob.os[0]))
    N.add_host(Host(3, 0, 110, 2, 0, [], glob.hardware[0], glob.processes[0:2], glob.services[0:2], glob.os[0]))

    for numb in range(1, numb1):
        N.add_host(Host(2, numb, 10, 2, 0, [], glob.hardware[0], glob.processes[0:2], glob.services[0:2], glob.os[0]))

    for numb in range(1, numb2):
        N.add_host(Host(3, numb, 10, 2, 0, [], glob.hardware[0], glob.processes[0:2], glob.services[0:2], glob.os[0]))

    N.add_sensitive_hosts((2,0))
    N.add_sensitive_hosts((3,1))
    N.add_sensitive_hosts((3,0))

    # Add the edges to the network.
    for numb in range(1, numb1):
        N.add_edge((1, 0), (2, numb), glob.services[0:1])
        N.add_edge((2, 0), (2, numb), glob.services[0:1])
        N.add_edge((2, numb), (2, 0), glob.services[0:1])

    for numb in range(1, numb2):
        N.add_edge((3, 0), (3, numb), glob.services[0:1])
        N.add_edge((3, numb), (3, 0), glob.services[0:1])

    N.add_edge((2, 0), (3, 0), glob.services[0:1])

    return N


def create_small_world(n, k, p, numb_process):
    """
    Creates a random graph and create a network based on the graph.
    Return the graph, the network and the positions.
    ----------
    n: int
        Number of hosts.
    k: int
        Each node is joined with its k nearest neighbors in a ring topology.
    p: int
        The probability of rewiring each edge
    numb_process: int
        The number of processes and services that hosts and edges should have.
        The number will be lower if there are less processes or services than
        asked for.
    """

    min_numb = min(numb_process, len(glob.services), len(glob.processes))
    if min_numb != numb_process:
        print(f"The number of processes and services is lowered to {min_numb}.")

    G = nx.watts_strogatz_graph(n, k, p, seed=3113794652)
    N = Network()

    # Add the hosts to the network
    for numb in range(0, len(G.nodes())):
        N.add_host(Host(2, numb, 10, 2, 0, [], glob.hardware[0], glob.processes[0:min_numb], glob.services[0:min_numb], glob.os[0]))

    # Add the edges to the network.
    # Add 1 to both source and destination because host 0 is the internet.
    for edge in G.edges():
        source, dest = edge
        N.add_edge(N.get_host_given_place(source+1).get_address(), N.get_host_given_place(dest+1).get_address(), glob.services[0:min_numb])
        N.add_edge(N.get_host_given_place(dest+1).get_address(), N.get_host_given_place(source+1).get_address(), glob.services[0:min_numb])

    # Connect the host that sybolises the internet to the network.
    if n >= 17:
        N.add_edge((1, 0), (2, 4), glob.services[0:min_numb])
        N.add_edge((1, 0), (2, 10), glob.services[0:min_numb])
        N.add_edge((1, 0), (2, 17), glob.services[0:min_numb])

        # Make some of the hosts sensitive hosts.
        N.add_sensitive_hosts((2,0))
        N.get_host((2,0)).change_score(100)

        N.add_sensitive_hosts((2,12))
        N.get_host((2,12)).change_score(200)


    return N


def create_power_law(n, k, p, numb_process):
    """
    Creates a random graph and create a network based on the graph.
    Return the graph, the network and the positions.
    ----------
    n: int
        Number of hosts.
    k: int
        The number of random edges to add for each new node
    p: int
        Probability of adding a triangle after adding a random edge
    numb_process: int
        The number of processes and services that hosts and edges should have.
        The number will be lower if there are less processes or services than
        asked for.
    """

    min_numb = min(numb_process, len(glob.services), len(glob.processes))
    if min_numb != numb_process:
        print(f"The number of processes and services is lowered to {min_numb}.")

    G = nx.powerlaw_cluster_graph(n, k, p, seed=3113794652)
    N = Network()

    # Add the hosts to the network.
    for numb in range(0, len(G.nodes())):
        N.add_host(Host(2, numb, 10, 2, 0, [], glob.hardware[0], glob.processes[0:min_numb], glob.services[0:min_numb], glob.os[0]))

    # Add the edges to the network.
    # Add 1 to both source and destination because host 0 is the internet.
    for edge in G.edges():
        source, dest = edge
        N.add_edge(N.get_host_given_place(source+1).get_address(), N.get_host_given_place(dest+1).get_address(), glob.services[0:min_numb])
        N.add_edge(N.get_host_given_place(dest+1).get_address(), N.get_host_given_place(source+1).get_address(), glob.services[0:min_numb])

    # Connect the host that sybolises the internet to the network.
    if n >= 18:
        N.add_edge((1, 0), (2, 10), glob.services[0:min_numb])
        N.add_edge((1, 0), (2, 13), glob.services[0:min_numb])
        N.add_edge((1, 0), (2, 14), glob.services[0:min_numb])
        N.add_edge((1, 0), (2, 18), glob.services[0:min_numb])

        # Make some of the hosts sensitive hosts.
        N.add_sensitive_hosts((2,0))
        N.get_host((2,0)).change_score(200)

        N.add_sensitive_hosts((2,2))
        N.get_host((2,2)).change_score(50)

        N.add_sensitive_hosts((2,5))
        N.get_host((2,5)).change_score(50)

    return N


def draw_network(network):
    G = nx.DiGraph(network.adjacency_matrix)
    pos = nx.spring_layout(G, seed=3113794652)  # positions for all nodes

    plt.figure()
    plt.title(str(glob.network_selection) + ", " + str(len(glob.attackers)) + " attacker(s), time: " + str(glob.MAX_RUNTIME))

    # Create the legend.
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Normal',markerfacecolor='tab:orange', markersize=10),
        Line2D([0], [0], marker='o', color='w', label='Hardened',markerfacecolor='tab:blue', markersize=10),
        Line2D([0], [0], marker='o', color='w', label='User comp',markerfacecolor='tab:red', markersize=10),
        Line2D([0], [0], marker='o', color='w', label='Admin comp',markerfacecolor='maroon', markersize=10),
    ]
    plt.legend(handles=legend_elements, loc='best')

    # Draw the normal and hardened hosts.
    nx.draw(G, pos, node_color="tab:orange")
    hardened_hosts = network.get_all_hardened_hosts()
    nx.draw(G, pos, nodelist=hardened_hosts, node_color="tab:blue")

    edges = G.edges
    colors = []

    # Set the color of all the edges.
    for u,v in edges:
        if network.get_edge_given_places(u, v).get_hardened() != []:
            colors.append("blue")
        else:
            colors.append("black")

    # Draw the compromised hosts and the hardened edges.
    compr_hosts_lvl1, compr_hosts_lvl2 = network.get_all_compromised_hosts()
    nx.draw(G, pos, nodelist=compr_hosts_lvl1, node_color="tab:red")
    nx.draw(G, pos, nodelist=compr_hosts_lvl2, node_color="maroon", edgelist=edges, edge_color=colors)

    labels = {}
    for n in G.nodes:
        add1, add2 = network.hosts[n].get_address()
        labels[n] = str(add1) + ", " + str(add2)

    nx.draw_networkx_labels(G, pos, labels, font_size=6, font_color="whitesmoke")
    plt.savefig(f"./{glob.OUT_FOLDERNAME}/Network_fig.png", format="PNG")
    plt.close()

if __name__ == '__main__':
    # N = create_basic_network(5, 3)
    N = create_small_world(20, 4, 0.8, 1)
    # N = create_power_law(20, 1, 0.4, 1)

    draw_network(N)
