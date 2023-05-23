import random
import globals as glob
import actions_att as act


class Attacker:
    """
    This is the class for the attacker.
    ...
    Attributes
    ----------
    env : Simpy Enviroment
        The Simpy enviroment of the simulator.
    network : Network
        The Netork with all the hosts and edges.
    process : Process
        The process of the attacker running.
    attacker_settings : []
        The attacker_settings consist of which strategy and actions are set.
    strategy : int
        The strategy chosen for the attacker
    compromised hosts : [hosts]
        The list with hosts which have been compromised by this attacker.
    score : AccessLevel,
        The won score by compromising the network for this attacker.
    """

    def __init__(self, env, network, attacker_settings):
        self.env = env
        self.network = network
        self.attacker_settings = attacker_settings
        self.strategy = ""
        self.actions = {}
        self.compromised_hosts = []
        self.scanned_hosts = []
        self.score = 0
        self.cost = 0
        self.start = (1, 0)
        self.target = (1, 0)


    def run(self):
        """
        The main process, which the attacker repeats untill the simulation is terminated.
        """
        # Load attacks to launch based on attack strategy
        self.load_actions()

        while True:
            if self.strategy == "Zero-day exploit":
                # Run ZDE
                yield self.env.process(self.zero_day_exploit())
            if self.strategy == glob.AttackStrat.APT:
                # Run ZDE
                continue
            if self.strategy == glob.AttackStrat.DOS:
                # Run ZDE
                continue


    def load_actions(self):
        """
        Load the actions for this attacker based on given strategy.
        """
        self.strategy = self.attacker_settings[0].get()
        if self.attacker_settings[1].get() == 1:
            self.actions["snscan"] = act.SubnetScan(10, 1) #Subnetscan with duration 10 and cost 1.
        if self.attacker_settings[2].get() == 1:
            self.actions["osscan"] = act.OSScan(5, 1) #Osscan with duration 5 and cost 1.
        if self.attacker_settings[3].get() == 1:
            self.actions["hwscan"] = act.HardwareScan(5, 1) #Hardwarescan with duration 5 and cost 1.
        if self.attacker_settings[4].get() == 1:
            self.actions["pscan"] = act.ProcessScan(5, 1) #Processscan with duration 5 and cost 1.
        if self.attacker_settings[5].get() == 1:
            self.actions["sscan"] = act.ServiceScan(5, 1) #Servicescan with duration 5 and cost 1.
        if self.attacker_settings[6].get() == 1:
            self.actions["exploit"] = glob.atts_e
        if self.attacker_settings[7].get() == 1:
            self.actions["priv_esc"] = glob.atts_h
        if self.attacker_settings[8].get() == 1:
            self.actions["dos"] = act.DenialOfService("dos", 1, 20, 10) #Denialofservice with duration 10 and cost 20.
        glob.logger.info(f"Attacker actions and strategy have been loaded for attacker at {self.env.now}.")


    def zero_day_exploit(self):
        """
        This is the zero-day exploit strategy where the focus is on using exploits to get deeper within the network.
        """
        # Check if host is already compromised.
        host = self.network.get_host(self.start)
        if host.get_attacker_access_lvl() == glob.AccessLevel.ROOT:
            # If so then scan for other hosts and to compromised nodes.
            self.compromised_hosts.append(self.start)
            glob.logger.info(f"Start SubnetScan at {self.env.now}.")
            yield self.env.process(self.subnetscan())

            # Check the edges for hardenning if none exploit etc...
            glob.logger.info(f"Start Exploit at {self.env.now}.")
            yield self.env.process(self.exploit())
        else:
            # Else run a privilege escalation.
            glob.logger.info(f"Start PrivilegeEscalation at {self.env.now}.")
            yield self.env.process(self.privilege_escalation(host))

    def advanced_persistant_threats(self):
        # Check if host is already compromised.
        host = self.network.get_host(self.start)
        if host.get_attacker_access_lvl() == glob.AccessLevel.ROOT:
            # If so then scan for other hosts and to compromised nodes.
            self.compromised_hosts.append(self.start)
            glob.logger.info(f"Start SubnetScan at {self.env.now}.")
            yield self.env.process(self.subnetscan())

            # Check the edges for hardenning if none exploit etc...
            glob.logger.info(f"Start Exploit at {self.env.now}.")
            yield self.env.process(self.exploit())
        else:
            # Else run a privilege escalation.
            glob.logger.info(f"Start PrivilegeEscalation at {self.env.now}.")
            yield self.env.process(self.privilege_escalation())

    def denial_of_service(self):
        # Check if host is already compromised.
        host = self.network.get_host(self.start)
        if host.get_attacker_access_lvl() == glob.AccessLevel.ROOT:
            # If so then scan for other hosts and to compromised nodes.
            self.compromised_hosts.append(self.start)
            glob.logger.info(f"Start SubnetScan at {self.env.now}.")
            yield self.env.process(self.subnetscan())

            # Check the edges for hardenning if none exploit etc...
            glob.logger.info(f"Start Exploit at {self.env.now}.")
            yield self.env.process(self.exploit())
        else:
            # Else run a privilege escalation.
            glob.logger.info(f"Start PrivilegeEscalation at {self.env.now}.")
            yield self.env.process(self.privilege_escalation())

    def subnetscan(self):
        """
        The subnet scan function which checks for reachable hosts.
        """
        yield self.env.timeout(self.actions["snscan"].get_duration())
        self.scanned_hosts = self.network.reachable_hosts(self.start)
        self.update_cost(self.actions["snscan"].get_cost())
        glob.logger.info(f"SubnetScan succeeded on host {self.start} at {self.env.now}.")

    def exploit(self):
        """
        The exploit function which tries to exploit a link to hop to another node.
        """
        vulnerable_edge = None
        seen_edges = [self.network.get_edge((self.start, host.get_address())) for host in self.scanned_hosts]
        for edge in seen_edges:
            if len(edge.possible_exploits()) > 0:
                vulnerable_edge = edge
                break

        # Failsafe if no edges can be exploited.
        if vulnerable_edge is None:
            return

        exploit = self.lowest_cost(vulnerable_edge.possible_exploits())
        self.update_cost(exploit.get_cost())

        yield self.env.timeout(exploit.get_duration())

        if exploit.get_name() in edge.get_hardened():
            glob.logger.info(f"Exploit failed on edge {vulnerable_edge.get_both_addr()} at {self.env.now}.")
            self.network.add_failed_att_edges(vulnerable_edge)
        else:
            glob.logger.info(f"Exploit succeeded on edge {vulnerable_edge.get_both_addr()} at {self.env.now}.")
            self.start = vulnerable_edge.get_source_addr()


    def privilege_escalation(self, host):
        """
        The privilege escalation function which tries to escalate privelege.
        """
        priv_esc = self.lowest_cost(host.possible_attacks())
        self.update_cost(priv_esc.get_cost())

        if priv_esc.get_name() in host.get_hardened():
            # Priv_esc has failed.
            yield self.env.timeout(priv_esc.get_duration())
            glob.logger.info(f"Privilege escalation failed on host {host.get_address()} at {self.env.now}.")
            self.network.add_failed_att_hosts(host)
        else:
            # Priv_esc has succeeded.
            yield self.env.timeout(priv_esc.get_duration())
            host.set_attacker_access_lvl(host.get_attacker_access_lvl() + 1)
            if host.get_attacker_access_lvl() == glob.AccessLevel.ROOT:
                self.update_score(host.get_score())
            glob.logger.info(f"Privilege escalation succeeded on host {host.get_address()} at {self.env.now}.")


    def update_cost(self, cost):
        """
        Update the cost of the attacker with given value for cost.
        """
        self.cost += cost


    def update_score(self, score):
        """
        Update the score of the attacker with given value for score.
        """
        self.score += score

    def lowest_cost(self, exploits):
        best_exploit = None
        for exploit in exploits:
            if best_exploit == None:
                best_exploit = exploit
            else:
                if exploit.get_cost() < best_exploit.get_cost():
                    best_exploit = exploit

        return best_exploit
