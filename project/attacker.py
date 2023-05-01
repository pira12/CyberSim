import random
import globals as glob
import actions as act


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
        self.target = (1, 0)


    def run(self):
        # Load attacks to launch based on attack strategy
        self.load_actions()

        while True:
            # TODO! : Check if host is already compromised.

                # TODO! : If so then scan for other hosts.

                # TODO! : Else run a privilege escalation.

            # TODO! : Check the edges for hardenning if none exploit etc...




            # TODO! : Run the attack on host
            glob.logger.info(f"Start {attack_type} at {self.env.now}.")
            # TODO! : Log the attack

            # Wait for the attack to finish
            yield self.env.timeout(10) # For now set to 10, but varies

            # If the attack succeeded increase score and Log it.
            if random.random() > 0.5:
                self.score += 10
                glob.logger.info(f"Start {attack_type} succeeded at {attack_start}.")



    def load_actions(self):
        """
        Load the actions for this attacker based on given strategy.
        """
        if self.strategy == glob.AttackStrat.RAND:
            self.actions = {
                "snscan" : act.SubnetScan(10, 1), #Subnetscan with duration 10 and cost 1.
                "osscan" : act.OSScan(5, 1), #Osscan with duration 5 and cost 1.
                "hwscan" : act.HardwareScan(5, 1), #Hardwarescan with duration 5 and cost 1.
                "pscan" : act.ProcessScan(5, 1), #Processscan with duration 5 and cost 1.
                "sscan" : act.ServiceScan(5, 1), #Servicescan with duration 5 and cost 1.
                "exploit" : act.Exploit("exploit", (1,0), 20, 10), #Exploit with duration 10 and cost 20.
                "priv_esc": act.PrivilegeEscalation("priv_esc", (1,0), 20, 10) #Privilegeescalation with duration 10 and cost 20.
            }


    def subnetscan(self):
        yield self.env.timeout(self.actions["snscan"].duration)
        self.seen_hosts += self.network.get_all_edges_from(self.target)

