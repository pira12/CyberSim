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
    attacker_settings : []
        The attacker_settings consist of which strategy and actions are set.
    id : int
        The attacker id set in the GUI
    strategy : string
        The strategy chosen for the attacker
    actions : {}
        A dictionary filled with the available attacks for the attacker.
    compromised_hosts : [hosts]
        The list with hosts which have been compromised by this attacker.
    scanned_hosts : [hosts]
        The list with hosts which have been scanned by this attacker.
    score : int
        The won score by compromising the network for this attacker.
    cost : int
        The lost score by performing actions.
    start : (int, int)
        The host where the attacker starts in a round.
    target : (int, int)
        The host where the attacker focusses on in a round.
    """

    def __init__(self, env, network, attacker_settings, attacker_id):
        self.env = env
        self.network = network
        self.attacker_settings = attacker_settings
        self.id = attacker_id
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
        # Load attacks to launch based on attack strategy.
        self.load_actions()
        self.add_compromised_host(((1, 0), 2))

        while True:
            glob.progress_bar.set(self.env.now / int(glob.MAX_RUNTIME))
            # print(self.compromised_hosts)
            if self.strategy == "Random Strategy":
                # Run RST
                yield self.env.process(self.random_strategy())
            if self.strategy == "Zero-day exploit":
                # Run ZDE
                yield self.env.process(self.zero_day_exploit())
            if self.strategy == "Advanced Persistent Threats":
                # Run APT
                yield self.env.process(self.advanced_persistant_threats())


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
        glob.logger.info(f"Attacker actions and strategy have been loaded for attacker {self.id} at {self.env.now}.")

    def random_strategy(self):
        """
        Random strategy for the attacker.
        """
        # Check if host is already compromised.
        host = self.network.get_host(self.start)

        if self.start != (1, 0):
            # Else run a privilege escalation.
            if random.randint(0, 1) > 0.5:
                glob.logger.info(f"Start PrivilegeEscalation at {self.env.now}.")
                yield self.env.process(self.privilege_escalation(host))

        if self.compromised_check(host.get_address()) != False or self.compromised_check(host.get_address()) == 2:
            # If so then scan for other hosts and to compromised nodes.
            glob.logger.info(f"Start SubnetScan at {self.env.now}.")
            yield self.env.process(self.subnetscan())

            # Choose a random target from seen hosts.
            self.target = random.choice(self.scanned_hosts).get_address()
            edge = self.network.get_edge((self.start, self.target))

            # Check if there are new hosts else end attack.
            if edge == None:
                self.start = random.choice(self.compromised_hosts)[0]
                glob.logger.info(f"Looping back to host {self.start} at {self.env.now}.")
            else:
                glob.logger.info(f"Start Exploit at {self.env.now}.")
                yield self.env.process(self.exploit(edge))


    def zero_day_exploit(self):
        """
        This is the zero-day exploit strategy where the focus is on using exploits to get deeper within the network.
        """
        # Make a temp host for the run.
        host = self.network.get_host(self.start)
        # If the host had more that 3 neighbors we think it is valuable so get score.
        if len(self.network.get_all_edges_from(self.start)) > 3:
            if self.start != (1, 0):
                # Run a privilege escalation.
                glob.logger.info(f"Start PrivilegeEscalation at {self.env.now}.")
                yield self.env.process(self.privilege_escalation(host))

        if self.compromised_check(host.get_address()) != False:
            # If so then scan for other hosts and to compromised nodes.
            glob.logger.info(f"Start SubnetScan at {self.env.now}.")
            yield self.env.process(self.subnetscan())

            # Choose the best target from seen hosts.
            self.target = self.get_best_target()
            edge = self.network.get_edge((self.start, self.target))

            # Check if there are new hosts else end attack.
            if edge == None:
                self.start = random.choice(self.compromised_hosts)[0]
                glob.logger.info(f"Looping back to host {self.start} at {self.env.now}.")
            else:
                glob.logger.info(f"Start Exploit at {self.env.now}.")
                yield self.env.process(self.exploit(edge))
            return

        if self.start != (1,0):
            # Else run a privilege escalation till you have the score.
            glob.logger.info(f"Start PrivilegeEscalation at {self.env.now}.")
            yield self.env.process(self.privilege_escalation(host))


    def advanced_persistant_threats(self):
        """
        This is the advanced persistant threat strategy where the focus is on gaining access on as many hots as possible.
        """
        # Make a temp host for the run.
        host = self.network.get_host(self.start)

        if self.compromised_check(host.get_address()) != 2:
            if self.start != (1, 0):
                # Run a privilege escalation till root level.
                glob.logger.info(f"Start PrivilegeEscalation at {self.env.now}.")
                yield self.env.process(self.privilege_escalation(host))
        else:
            # If so then scan for other hosts and to compromised nodes.
            glob.logger.info(f"Start SubnetScan at {self.env.now}.")
            yield self.env.process(self.subnetscan())

            # Choose the best target from seen hosts.
            self.target = self.get_low_lvl_target()
            edge = self.network.get_edge((self.start, self.target))

            # Check if there are new hosts else end attack.
            if edge == None:
                self.start = random.choice(self.compromised_hosts)[0]
                glob.logger.info(f"Looping back to host {self.start} at {self.env.now}.")
            else:
                glob.logger.info(f"Start Exploit at {self.env.now}.")
                yield self.env.process(self.exploit(edge))


    def subnetscan(self):
        """
        The subnet scan function which checks for reachable hosts.
        """
        yield self.env.timeout(self.actions["snscan"].get_duration())
        # After waiting scan the hosts and update scanned hosts list.
        self.scanned_hosts = self.network.reachable_hosts(self.start)
        self.update_cost(self.actions["snscan"].get_cost())
        glob.logger.info(f"SubnetScan succeeded on host {self.start} at {self.env.now}.")

    def exploit(self, vulnerable_edge):
        """
        The exploit function which tries to exploit a link to hop to another node.
        """
        exploit = self.lowest_cost(vulnerable_edge.possible_exploits())
        yield self.env.timeout(5)

        # Try to start an exploit if it fails then that means the defender was quicker.
        try:
            self.update_cost(exploit.get_cost())
            yield self.env.timeout(exploit.get_duration())
        except:
            glob.logger.info(f"Exploit failed on edge {vulnerable_edge.get_both_addr()} at {self.env.now}.")
            self.network.add_failed_att_edges(vulnerable_edge)
            return

        # Continue with registering the exploit in the network and adding the score to the attacker.
        if exploit.get_name() in vulnerable_edge.get_hardened() and exploit.get_prob() >= random.randint(0,1):
            glob.logger.info(f"Exploit failed on edge {vulnerable_edge.get_both_addr()} at {self.env.now}.")
            self.network.add_failed_att_edges(vulnerable_edge)
        else:
            glob.logger.info(f"Exploit succeeded on edge {vulnerable_edge.get_both_addr()} at {self.env.now}.")
            self.add_compromised_host((vulnerable_edge.get_dest_addr(), 0))
            self.start = vulnerable_edge.get_dest_addr()


    def privilege_escalation(self, host):
        """
        The privilege escalation function which tries to escalate privelege.
        """
        priv_esc = self.lowest_cost(host.possible_attacks())
        yield self.env.timeout(5)

        # Try to start an priv_esc if it fails then that means the defender was quicker.
        try:
            self.update_cost(priv_esc.get_cost())
            yield self.env.timeout(priv_esc.get_duration())
        except:
            # Priv_esc has failed.
            glob.logger.info(f"Privilege escalation failed on host {host.get_address()} at {self.env.now}.")
            self.network.add_failed_att_hosts(host)
            self.start = (random.choice(self.compromised_hosts)[0])
            return

        if priv_esc.get_name() in host.get_hardened() and priv_esc.get_prob() >= random.randint(0,1):
            # Priv_esc has failed.
            glob.logger.info(f"Privilege escalation failed on host {host.get_address()} at {self.env.now}.")
            self.network.add_failed_att_hosts(host)
        else:
            # Priv_esc has succeeded.
            host.set_attacker_access_lvl(host.get_attacker_access_lvl() + 1)
            self.add_compromised_host((host.get_address(), 1))
            if host.get_attacker_access_lvl() == glob.AccessLevel.ROOT:
                self.add_compromised_host((host.get_address(), 2))
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
        """
        This function will return the exploit with the lowest cost.
        """
        best_exploit = None
        for exploit in exploits:
            if best_exploit == None:
                best_exploit = exploit
            else:
                if exploit.get_cost() < best_exploit.get_cost():
                    best_exploit = exploit

        return best_exploit

    def add_compromised_host(self, item):
        """
        Add a new compromised host to the list or update existing host with higher acces level.
        """
        for i, host in enumerate(self.compromised_hosts):
            if item[0] == host[0]:
                if item[1] == host[1]:
                    return
                if item[1] > host[1]:
                    self.compromised_hosts[i] = (item[0], item[1])
                    return
                return

        # This is if it is not in the list.
        self.compromised_hosts.append(item)

    def get_best_target(self):
        """
        This function should prioritise hosts from other subnets, if there is none, just take one.
        """
        for host in self.scanned_hosts:
            if host.get_address()[0] != self.start[0]:
                return host.get_address()

        return random.choice(self.scanned_hosts).get_address()

    def get_low_lvl_target(self):
        """
        This function should prioritise hosts with low acces lvl if there is none, just take one.
        """
        for host in self.scanned_hosts:
            if self.compromised_check(host.get_address()) == False:
                return host.get_address()
            if self.compromised_check(host.get_address()) < 2:
                return host.get_address()

        return random.choice(self.scanned_hosts).get_address()

    def compromised_check(self, address):
        """
        This function will check if the adress is in compromised_hosts or not.
        If it is return acces_lvl else return false.
        """
        for host in self.compromised_hosts:
            if host[0] == address:
                return host[1]

        return False