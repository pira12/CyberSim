import random
import simpy
from actions_def import Harden_host, Harden_edge
from actions_att import Exploit, PrivilegeEscalation
import globals as glob

# glob_atts_h = [PrivilegeEscalation("att_h1", 1, 10, 0.8, 1, process="p1")]
# glob_atts_e = [Exploit("att_e1", 1, 10, 0.8, service="s1")]

# glob_hard_h = [Harden_host("harden att_h1", 1, 10, "att_h1"), Harden_host("harden att_h2", 1, 10, "att_h2"), Harden_host("harden att_h3", 1, 10, "att_h3")]
# glob_hard_e = [Harden_edge("harden att_e1", 1, 1, "att_e1"), Harden_edge("harden att_e2", 1, 1, "att_e2"), Harden_edge("harden att_e3", 1, 10, "att_e3")]

# first-layer defense
# last-layer defense
# minimum-cost defense en dan ook voor duration I guess... of kan alles tegelijk hmmmm

def log_scores(attackers, defender, network, env):

    while True:

        if env.now == 20:
            print("oi")
            glob.atts_h.append(PrivilegeEscalation("host_att3", 0.5, 10, 0.8, 1, process="p1"))

        max_score, compromised_score = network.calculate_score()
        def_cost = defender.get_cost()
        glob.score_logger.info(f"{env.now} Defender damage {compromised_score} actions cost {def_cost}")

        for i, attacker in enumerate(attackers):
            glob.score_logger.info(f"{env.now} Attacker{i} score {attacker.score} actions cost {attacker.cost}")

        yield env.timeout(1)


class Defender:
    def __init__(self, env, network, strategy):
        self.env = env
        self.network = network
        self.strategy = strategy
        self.cost = 0
        self.harden_host_allowed = glob.harden_host_allowed.get()
        self.harden_edge_allowed = glob.harden_edge_allowed.get()

        self.failed_att_hosts = [] #hmmmmm, nodig?
        self.failed_att_edges = [] #hmmmmm, nodig?


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
        random = Randomly harden edges and hosts.
        last_def = Harden first the sensitive hosts against the relevant
                   Privilege Escalations. Then harden the edges towards the
                   sensitive hosts against exploits. Do random hardenings
                   afterwards.
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

        max_host = self.network.get_number_of_hosts()
        random_numb = random.randint(0, max_host-1)

        # Determine the most connected neighbour and the most connected
        # neighbour of the most connected neighbour.
        best1 = self.network.get_most_connected_neighbour(random_numb)
        best2 = self.network.get_most_connected_neighbour(best1)

        # Depending on what is allowed, do an edge hardening or host hardening.
        # Edge hardening is tried first.
        if not self.get_harden_edge_allowed():
            yield self.env.process(self.fully_harden_host(self.network.get_host_given_place(best2), 1))
        else:
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

        # print(self.network.get_host_given_place(random_numb).get_address(),self.network.get_host_given_place(best1).get_address(), self.network.get_host_given_place(best2).get_address())


    def lazy_defense(self, if_noone):
        """
        Only harden the hosts/edges which had a failed attack.
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
                yield self.env.process(self.fully_harden_host(host, 0))

        for edge in att_edges:
            self.add_failed_att_edges(edge)
            if self.get_harden_edge_allowed():
                yield self.env.process(self.fully_harden_edge(edge, 0))

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

        for imp in importants:
            if self.get_harden_host_allowed():
                yield self.env.process(self.fully_harden_host(imp, 0))

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
                self.env.timeout(0.1)
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
                self.env.timeout(0.1)
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
        """
        exploit_names = edge.possible_exploits_names()

        useful_harden = []
        for possible_harden in glob.hard_e:
            if possible_harden.get_attack_type() in exploit_names:
                useful_harden.append(possible_harden)

        return useful_harden

    def get_random_def_h(self):
        return random.choice(glob.hard_h)

    def get_random_def_e(self):
        return random.choice(glob.hard_e)


    def random_defense(self):
        """
        Add a defense to a random host or edge.
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


    def double_random_defense(self):
        """
        Add a defense to a random host or edge.
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
            yield self.env.process(self.harden_host(random_host, self.get_random_def_h()))

        else:
            random_edge = self.network.get_random_edge()
            yield self.env.process(self.harden_edge(random_edge, self.get_random_def_e()))


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
