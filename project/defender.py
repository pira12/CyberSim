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

class Defender:
    def __init__(self, env, network, strategy):
        self.env = env
        self.network = network
        self.strategy = strategy
        self.score = 0


    def get_score(self):
        return self.score


    def subtract_score(self, numb):
        """
        Subtract a number from the score.
        """
        self.score -= numb


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

        if self.strategy == "random":
            # while True:
            #     yield self.env.process(self.random_defense())
            yield self.env.process(self.first_layer_defense())

            yield self.env.process(self.last_layer_defense())

            while True:
                yield self.env.process(self.random_defense())


    def first_layer_defense(self):
        """
        Harden the first layer
        """

        att_hosts = self.network.get_failed_att_hosts()
        # att_edges = self.network.get_failed_att_edge()
        att_edges = [self.network.get_edge(((1,0), (2,2)))]
        print(att_edges)

        if att_edges != []:
            yield self.env.process(self.fully_harden_edge(att_edges[0]))
        else:
            yield self.env.process(self.random_defense())


    def last_layer_defense(self):
        """
        Harden first the sensitive hosts against the relevant
        Privilege Escalations. Then harden the edges towards the
        sensitive hosts against exploits.
        """
        importants = self.network.get_sensitive_hosts2()

        for imp in importants:
            yield self.env.process(self.fully_harden_host(imp))

        for imp in importants:
            out_going = self.network.get_all_edges_to(imp.get_address())

            for out in out_going:
                yield self.env.process(self.fully_harden_edge(out))


    def fully_harden_host(self, host):
        """
        Use all relevant hardenings on the given host.
        host : Host
        """
        useful = self.get_useful_hardenings_host(host)

        for u in useful:
            yield self.env.process(self.harden_host(host, u))


    def get_useful_hardenings_host(self, host):
        """
        Determine and return which hardenings are useful.
        This is done by looking which attacks can be performed
        on this host. Hardenings that target those attacks are
        the useful hardenings.
        host : Host
        """
        attack_names = host.possible_attacks_names()

        useful_harden = []
        for possible_harden in glob.hard_h:
            if possible_harden.get_attack_type() in attack_names:
                useful_harden.append(possible_harden)

        return useful_harden


    def fully_harden_edge(self, edge):
        """
        Use all relevant hardenings on the given edge.
        edge : Edge
        """
        useful = self.get_useful_hardenings_edge(edge)

        for u in useful:
            yield self.env.process(self.harden_edge(edge, u))


    def get_useful_hardenings_edge(self, edge):
        """
        Determine and return which hardenings are useful.
        This is done by looking which exploits can be performed
        on this edge. Hardenings that target those exploits are
        the useful hardenings.
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
        """
        if random.random() >= 0.5:
            random_host = self.network.get_random_host()
            yield self.env.process(self.harden_host(random_host, self.get_random_def_h()))

        else:
            random_edge = self.network.get_random_edge()
            yield self.env.process(self.harden_edge(random_edge, self.get_random_def_e()))


    def harden_host(self, target_host, harden_action):
        """
        Harden a host against a certain type of attack.
        target_host : Host
        harden_action : Harden_host
        """
        glob.logger.info(f"Start Harden_host at {self.env.now} on host {target_host.get_address()}.")
        yield self.env.timeout(harden_action.get_duration())
        target_host.harden(harden_action.get_attack_type())

        self.subtract_score(harden_action.get_cost())
        glob.logger.info(f"Host {target_host.get_address()} hardened against {harden_action.get_attack_type()} at {self.env.now}.")


    def harden_edge(self, target_edge, harden_action):
        """
        Harden an edge against a certain type of attack.
        target_edge : Edge
        harden_action : Harden_edge
        """
        glob.logger.info(f"Start Harden_edge at {self.env.now} on edge {target_edge.get_both_addr()}.")
        yield self.env.timeout(harden_action.get_duration())
        target_edge.harden(harden_action.get_attack_type())

        self.subtract_score(harden_action.get_cost())
        glob.logger.info(f"Edge {target_edge.get_both_addr()} hardened against {harden_action.get_attack_type()} at {self.env.now}.")
