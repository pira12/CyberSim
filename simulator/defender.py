import random
import globals as glob


class Defender:
    """
    The class for the defender of the network.
    There is only one defender per network.
    ----------
    env : Simpy Environment
        The Simpy enviroment of the simulator.
    network: Network
        The Netork with all the hosts and edges.
    strategy: string
        The strategy the defender is using to defend the network.
    cost: int
        The total cost of all actions taken by the defender.
    harden_host_allowed: int
        Indicates if host hardening is allowed.
            0 means it is not allowed
            1 means it is allowed
    harden_edge_allowed: int
        Indicates if edge hardening is allowed.
            0 means it is not allowed
            1 means it is allowed
    scan_allowed: int
        Indicates if scanning is allowed.
            0 means it is not allowed
            1 means it is allowed
        It is not currently being used.
    update_firewall_allowed: int
        Indicates if updating firewalls is allowed.
            0 means it is not allowed
            1 means it is allowed
        It is not currently being used.
    update_host_allowed: int
        Indicates if updating hosts is allowed.
            0 means it is not allowed
            1 means it is allowed
        It is not currently being used.
    failed_att_hosts : [(int, int)]
        An array with all (subnet addr, host addr) of the hosts that
        have been attack, but the attack failed.
        It is not currently being used.
    failed_att_edges : [((int, int), (int, int))]
        An array with all (source addr, destination addr) of the edges
        that have been attack, but the attack failed.
        It is not currently being used.
    """
    def __init__(self, env, network, strategy):
        self.env = env
        self.network = network
        self.strategy = strategy
        self.cost = 0
        self.harden_host_allowed = glob.harden_host_allowed.get()
        self.harden_edge_allowed = glob.harden_edge_allowed.get()

        self.scan_allowed = glob.scan_host_allowed.get()                    # Not used
        self.update_firewall_allowed = glob.update_firewall_allowed.get()   # Not used
        self.update_host_allowed = glob.update_host_allowed.get()           # Not used
        self.failed_att_hosts = []                                          # Not used
        self.failed_att_edges = []                                          # Not used


    def get_scan_cost(self):
        """
        Return the scan_cost of the defender.
        """
        return self.scan_cost


    def get_scan_duration(self):
        """
        Return the scan_duration of the defender.
        """
        return self.scan_duration


    def get_cost(self):
        """
        Return the score of the defender.
        """
        return self.cost


    def add_cost(self, numb):
        """
        Add the number to the cost.
        ----------
        numb: int
        """
        self.cost += numb

    def get_strategy(self):
        """
        Return the strategy of the defender.
        """
        return self.strategy

    def get_failed_att_hosts(self):
        """
        Return the hosts that have been the target of a failed attack.
        """
        return self.failed_att_hosts


    def add_failed_att_hosts(self, host):
        """
        Add a new failed attack on a host.
        ----------
        host: Host
            The host that was target of a new failed attack.
        """
        self.failed_att_hosts.append(host)


    def get_failed_att_edges(self):
        """
        Return the hosts that have been the target of a failed attack.
        """
        return self.failed_att_edges


    def add_failed_att_edges(self, edge):
        """
        Add a new failed attack on a edge.
        ----------
        edge: Edge
            The edge that was target of a new failed attack.
        """
        self.failed_att_edges.append(edge)


    def get_harden_host_allowed(self):
        """
        Return whether hosts can be hardened.
        """
        return self.harden_host_allowed


    def get_harden_edge_allowed(self):
        """
        Return whether edges can be hardened.
        """
        return self.harden_edge_allowed


    def run(self):
        """
        The main process, which the attacker repeats until the simulation
        is terminated.
        random: Randomly fully harden edges and hosts.

        last layer: Harden first the sensitive hosts against the relevant
            Privilege Escalations. Then harden the edges towards the
            sensitive hosts against exploits. Do random hardenings
            afterwards.

        minimum: Only fully harden hosts or edges that have been the target
            of failed attacks.

        reactive and random: A combination of random and minimum.
            Random hosts and edges are fully hardened, until a failed
            attack is noticed. The target of that attack is then fully
            hardened. This is repeated indefinitely.

        highest degree neighbour: Prioritises hosts with a lot of edges.
            A random host is chosen.
            The neighbour of that host with the most edges is best1.
            The neighbour of host best1 with the most edges is best2.
            An edge between best1 and best2 is fully hardened,
            or either best1 or best2 is hardened.
        """

        if self.get_strategy() == "random":
            while True:
                yield self.env.process(self.random_defense())

        elif self.get_strategy() == "last layer":
            yield self.env.process(self.last_layer_defense())

            while True:
                yield self.env.process(self.random_defense())

        elif self.get_strategy() == "minimum":
            while True:
                yield self.env.process(self.lazy_defense(1))

        elif self.get_strategy() == "reactive and random":
            while True:
                yield self.env.process(self.lazy_defense(2))

        elif self.get_strategy() == "highest degree neighbour":
            while True:
                yield self.env.process(self.highest_degree_def())


    def highest_degree_def(self):
        """
        A defensive strategy that prioritises hosts with a lot of edges.
        A random host is chosen.
        The neighbour of that host with the most edges is best1.
        The neighbour of host best1 with the most edges is best2.
        An edge between best1 and best2 is fully hardened,
        or either best1 or best2 is hardened.
        """
        high_deg = self.network.get_most_connected_host()

        # Determine the most connected neighbour and the most connected
        # neighbour of the most connected neighbour.
        best1 = self.network.get_most_connected_neighbour(high_deg)
        best2 = self.network.get_most_connected_neighbour(best1)

        r = random.randint(0, 1)

        # Depending on what is allowed, do an edge hardening or host hardening.
        # Edge hardening is tried first.
        if not self.get_harden_edge_allowed():
            yield self.env.process(self.fully_harden_host(self.network.get_host_given_place(best2), 1))
        elif not self.get_harden_host_allowed() or r:
            the_edge = None

            # Determine in which direction the edge between the neighbours
            # will be hardened.
            if self.network.check_edge(best1, best2) and self.network.check_edge(best2, best1):
                if random.randint(0, 1):
                    the_edge = self.network.get_edge_given_places(best1, best2)
                else:
                    the_edge = self.network.get_edge_given_places(best2, best1)

            elif self.network.check_edge(best1, best2):
                the_edge = self.network.get_edge_given_places(best1, best2)

            elif self.network.check_edge(best2, best1):
                the_edge = self.network.get_edge_given_places(best2, best1)

            else:
                print("Two neighbours do not have any connection, something went wrong.")
                exit(1)

            yield self.env.process(self.fully_harden_edge(the_edge, 1))
        else:
            yield self.env.process(self.fully_harden_host(self.network.get_host_given_place(best2), 1))


    def lazy_defense(self, if_noone):
        """
        Harden the hosts/edges which had a failed attack.
        Also save which hosts/edges have been attacked.
        ----------
        if_noone : int
            What to do when there is no new failed attack
            0: nothing
            1: wait
            2: do a random hardening
            else: nothing
        """

        att_hosts = self.network.get_failed_att_hosts()
        att_edges = self.network.get_failed_att_edges()

        for host in att_hosts:
            self.add_failed_att_hosts(host)

            if self.get_harden_host_allowed():
                yield self.env.process(self.fully_harden_host(self.network.get_host(host), 0))

        for edge in att_edges:
            self.add_failed_att_edges(edge)

            if self.get_harden_edge_allowed():
                yield self.env.process(self.fully_harden_edge(self.network.get_edge(edge), 0))

        self.network.reset_failed_att_hosts()
        self.network.reset_failed_att_edges()

        # What to do if there was no failed attack.
        if att_hosts == [] and att_edges == []:
            if if_noone == 1:
                yield self.env.timeout(0.5)
            elif if_noone == 2:
                yield self.env.process(self.random_defense())


    def last_layer_defense(self):
        """
        Harden first the sensitive hosts against the relevant
        Privilege Escalations. Then harden the edges towards the
        sensitive hosts against exploits.
        """
        importants = self.network.get_sensitive_hosts2()

        # First harden the sensitive host.
        for imp in importants:
            if self.get_harden_host_allowed():
                yield self.env.process(self.fully_harden_host(imp, 0))

        # Then harden all incoming edges of the sensitive hosts.
        for imp in importants:
            if self.get_harden_edge_allowed():
                incoming = self.network.get_all_edges_to(imp.get_address())

                for income in incoming:
                    yield self.env.process(self.fully_harden_edge(income, 0))


    def fully_harden_host(self, host, if_fail):
        """
        Use all relevant hardenings on the given host.
        Wait a little bit if there are none to prevent infinite loops
        when everything is already hardened.
        ----------
        host : Host
            The host that is fully hardened.
        if_fail: int
            What to do when the host could not be hardened:
            0: wait a short time
            1: do a random hardening instead
        """
        useful = self.get_useful_hardenings_host(host)

        for u in useful:
            yield self.env.process(self.harden_host(host, u))

        if useful == []:
            if if_fail == 0:
                yield self.env.timeout(0.1)
            if if_fail == 1:
                yield self.env.process(self.random_defense())


    def get_useful_hardenings_host(self, host):
        """
        Determine and return which hardenings are useful.
        This is done by looking which attacks can be performed
        on this host. Hardenings that target those attacks are
        the useful hardenings.
        ----------
        host : Host
            The host for which useful hardenings are determined.
        """
        attack_names = host.possible_attacks_names()

        useful_harden = []
        for possible_harden in glob.hard_h:
            if possible_harden.get_attack_type() in attack_names:
                useful_harden.append(possible_harden)

        return useful_harden


    def fully_harden_edge(self, edge, if_fail):
        """
        Use all relevant hardenings on the given edge.
        Wait a little bit if there are none to prevent infinite loops
        when everything is already hardened.
        ----------
        edge : Edge
            The edge that is fully hardened.
        if_fail: int
            What to do when the edge could not be hardened:
            0: wait a short time
            1: do a random hardening instead
        """
        useful = self.get_useful_hardenings_edge(edge)

        for u in useful:
            yield self.env.process(self.harden_edge(edge, u))

        if useful == []:
            if if_fail == 0:
                yield self.env.timeout(0.1)
            if if_fail == 1:
                yield self.env.process(self.random_defense())


    def get_useful_hardenings_edge(self, edge):
        """
        Determine and return which hardenings are useful.
        This is done by looking which exploits can be performed
        on this edge. Hardenings that target those exploits are
        the useful hardenings.
        ----------
        edge : Edge
            The edge for which useful hardenings are determined.
        """
        exploit_names = edge.possible_exploits_names()

        useful_harden = []
        for possible_harden in glob.hard_e:
            if possible_harden.get_attack_type() in exploit_names:
                useful_harden.append(possible_harden)

        return useful_harden


    def random_defense(self):
        """
        Fully harden a random host or edge.
        It is assumed that either hosts or edges are allowed
        to be hardened, or both.
        """
        threshold = 0.5
        if not self.get_harden_host_allowed():
            threshold = 1
        elif not self.get_harden_edge_allowed():
            threshold = 0

        if random.random() >= threshold:
            random_host = self.network.get_random_host()
            yield self.env.process(self.fully_harden_host(random_host, 0))

        else:
            random_edge = self.network.get_random_edge()
            yield self.env.process(self.fully_harden_edge(random_edge, 0))


    def harden_host(self, target_host, harden_action):
        """
        Harden a host against a certain type of attack.
        ----------
        target_host : Host
        harden_action : Harden_host
        """
        glob.logger.info(f"Start Harden_host on host {target_host.get_address()} at {self.env.now}.")
        yield self.env.timeout(harden_action.get_duration())
        target_host.harden(harden_action.get_attack_type())

        self.add_cost(harden_action.get_cost())
        glob.logger.info(f"Host {target_host.get_address()} hardened against {harden_action.get_attack_type()} at {self.env.now}.")


    def harden_edge(self, target_edge, harden_action):
        """
        Harden an edge against a certain type of attack.
        ----------
        target_edge : Edge
        harden_action : Harden_edge
        """
        glob.logger.info(f"Start Harden_edge on edge {target_edge.get_both_addr()} at {self.env.now}.")
        yield self.env.timeout(harden_action.get_duration())
        target_edge.harden(harden_action.get_attack_type())

        self.add_cost(harden_action.get_cost())
        glob.logger.info(f"Edge {target_edge.get_both_addr()} hardened against {harden_action.get_attack_type()} at {self.env.now}.")


    def scan_host(self, scan, target_host):
        """
        Scan a target host to check if the host is in any way compromised.
        The scanning action is never used in any strategy, thus
        this function is never used.
        """
        yield self.env.timeout(scan.get_duration())
        self.add_cost(scan.get_cost())

        if target_host.get_attacker_access_lvl() == 0:
            return 0
        else:
            return 1


    def update_host(self, host_update, target_host):
        """
        The processes of the target host are updated. This means that
        the host will take the processes of the host_update as its new
        processes.
        The update host action is never used in any strategy, thus
        this function is never used.
        """
        yield self.env.timeout(host_update.get_duration())
        self.add_cost(host_update.get_cost())

        target_host.update_processes(host_update.get_new_processes)


    def update_firewall(self, firewall_update, target_edge):
        """
        The services that are allowed on the target edge are updated.
        This means that the edge will take the services of the firewall_update
        as its new servs_allowed.
        The update firewall action is never used in any strategy, thus
        this function is never used.
        """
        yield self.env.timeout(firewall_update.get_duration())
        self.add_cost(firewall_update.get_cost())

        target_edge.update_servs_allowed(firewall_update.get_new_processes)
