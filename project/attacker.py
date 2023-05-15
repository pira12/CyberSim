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
    strategy : int
        The strategy chosen for the attacker
    compromised hosts : [hosts]
        The list with hosts which have been compromised by this attacker.
    score : AccessLevel,
        The won score by compromising the network for this attacker.
    """

    def __init__(self, env, network, strategy):
        self.env = env
        self.network = network
        self.strategy = strategy
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


    def load_actions(self):
        """
        Load the actions for this attacker based on given strategy.
        """
        glob.logger.info(f"Load attacker actions for strategy {self.strategy} at {self.env.now}.")
        if self.strategy == glob.AttackStrat.RAND:
            self.actions = {
                "snscan" : act.SubnetScan(10, 1), #Subnetscan with duration 10 and cost 1.
                "osscan" : act.OSScan(5, 1), #Osscan with duration 5 and cost 1.
                "hwscan" : act.HardwareScan(5, 1), #Hardwarescan with duration 5 and cost 1.
                "pscan" : act.ProcessScan(5, 1), #Processscan with duration 5 and cost 1.
                "sscan" : act.ServiceScan(5, 1), #Servicescan with duration 5 and cost 1.
                "exploit" : act.Exploit("exploit", 1, 20, 10), #Exploit with duration 10 and cost 20.
                "priv_esc": act.PrivilegeEscalation("priv_esc", 1, 20, 10) #Privilegeescalation with duration 10 and cost 20.
            }


    def subnetscan(self):
        """
        The subnet scan function which checks for reachable hosts.
        """
        yield self.env.timeout(self.actions["snscan"].get_duration())
        self.scanned_hosts = self.network.reachable_hosts(self.start)
        self.update_cost(self.actions["snscan"].get_cost())
        glob.logger.info(f"SubnetScan succeeded on host {self.start} at {self.env.now}.")


    def privilege_escalation(self):
        """
        The privilege escalation function which tries to escalate privelege.
        """
        host = self.network.get_host(self.start)
        self.update_cost(self.actions["priv_esc"].get_cost())

        if self.actions["priv_esc"].name in host.get_hardened():
            # Priv_esc has failed.
            yield self.env.timeout(self.actions["priv_esc"].get_duration())
            glob.logger.info(f"Privilege escalation failed on host {host.get_address()} at {self.env.now}.")
            self.network.add_failed_att_hosts(host)
        else:
            # Priv_esc has succeeded.
            yield self.env.timeout(self.actions["priv_esc"].get_duration())
            host.set_attacker_access_lvl(host.get_attacker_access_lvl() + 1)
            if host.get_attacker_access_lvl() == glob.AccessLevel.ROOT:
                self.update_score(host.get_score())
            glob.logger.info(f"Privilege escalation succeeded on host {host.get_address()} at {self.env.now}.")



    def exploit(self):
        """
        The exploit function which tries to exploit a link to hop to another node.
        """
        self.target = random.choice(self.scanned_hosts).get_address()
        edge = self.network.get_edge((self.start, self.target))
        self.update_cost(self.actions["exploit"].get_cost())

        yield self.env.timeout(self.actions["exploit"].get_duration())

        if self.actions["exploit"].name in edge.get_hardened():
            glob.logger.info(f"Exploit failed on edge {(self.start, self.target)} at {self.env.now}.")
            self.network.add_failed_att_edges(edge)
        else:
            glob.logger.info(f"Exploit succeeded on edge {(self.start, self.target)} at {self.env.now}.")
            self.start = self.target


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