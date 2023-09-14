import simpy
import sys
import copy
import globals as glob
import network as nw
import attacker as att
import defender as defend
from plot_log import draw_plot


def generate_network():
    """
    Generates network according to selected network in GUI.
    """
    if glob.use_created_network == True:
        return copy.deepcopy(glob.created_network)
    elif glob.network_selection == "network1":
        return nw.create_basic_network(5, 3)
    elif glob.network_selection == "network2":
        return nw.create_power_law(20, 1, 0.4, 1)
    elif glob.network_selection == "network3":
        return nw.create_power_law(20, 1, 0.4, 2)
    elif glob.network_selection == "network4":
        return nw.create_small_world(20, 4, 0.8, 1)
    elif glob.network_selection == "network5":
        return nw.create_small_world(20, 4, 0.8, 2)


def generate_attackers(env, N):
    """
    This funtion will generate the right amount of attackers with the information we  got from the GUI.
    ...
    Attributes
    ----------
    env : Simpy Enviroment
        The Simpy enviroment of the simulator.
    N : Network
        The Netork with all the hosts and edges.
    """
    glob.attackers = []
    for id, attacker_settings in enumerate(glob.attacker_list):
        attacker  = att.Attacker(env, N, attacker_settings, id)
        glob.attackers.append(attacker)
        env.process(attacker.run())

def generate_defender(env, N):
    """
    This funtion will generate the defender with the information we got from the GUI.
    ...
    Attributes
    ----------
    env : Simpy Enviroment
        The Simpy enviroment of the simulator.
    N : Network
        The Netork with all the hosts and edges.
    """
    defender  = defend.Defender(env, N, glob.defender_strategy.get())
    env.process(defender.run())
    return defender


def log_scores(attackers, defender, network, env):
    """
    A function that logs the scores of the attackers and defender regularly.
    ----------
    attackers: [Attacker]
        An array with all attackers.
    defender: Defender
        The defender of the network.
    network: Network
        The Netork with all the hosts and edges.
    env : Simpy Enviroment
        The Simpy enviroment of the simulator.
    """

    while True:
        # Use an if-statement to do something at a particular time.
        # In that if-statement, add attacks or hardenngs to the array
        # in globals to create an event.
        # if env.now == 20:
        #     glob.atts_h.append(PrivilegeEscalation("host_att3", 0.5, 10, 0.8, 1, process="p1"))

        _, compromised_score = network.calculate_score()
        def_cost = defender.get_cost()
        glob.score_logger.info(f"{env.now} Defender damage {compromised_score} actions cost {def_cost}")

        for i, attacker in enumerate(attackers):
            glob.score_logger.info(f"{env.now} Attacker{i} score {attacker.score} actions cost {attacker.cost}")

        yield env.timeout(1)


def stop_simulation():
    """
    Function which will stop the simulation.
    """
    sys.exit("Simulation was terminated by the user!")

def start_simulation():
    """
    Function which will start the simulation.
    """

    N = generate_network()

    #Create the Simpy enviroment
    env = simpy.Environment()


    # Create attackers and defenders.
    generate_attackers(env, N)

    defender = generate_defender(env, N)

    env.process(log_scores(glob.attackers, defender, N, env))

    # Run the simulation with multiple termination cireteria.
    env.run(until=glob.MAX_RUNTIME)

    glob.logger.info(f"Simulation ended at time: {env.now}")

    max_score, compromised_score = N.calculate_score()
    def_cost = defender.get_cost()

    # This part handles multiple runs.
    if glob.NUM_SIMS > 1:
        glob.max_score += max_score
        glob.compromised_score += compromised_score
        glob.def_cost += def_cost
        glob.def_total_cost += def_cost + compromised_score

        if glob.att_scores == [] or glob.att_costs ==[]:
            glob.att_scores = [0 for _ in range(len(glob.attackers))]
            glob.att_costs = [0 for _ in range(len(glob.attackers))]

        # print(glob.att_scores)
        # print(glob.att_costs)
        # print(len(glob.attackers))

        for i, attacker in enumerate(glob.attackers):
            glob.att_scores[i] += attacker.score
            glob.att_costs[i] += attacker.cost

    else:
        glob.max_score = max_score
        glob.compromised_score = compromised_score
        glob.def_cost = def_cost
        glob.def_total_cost = def_cost + compromised_score

        glob.att_scores = [0 for _ in range(len(glob.attackers))]
        glob.att_costs = [0 for _ in range(len(glob.attackers))]

        for i, attacker in enumerate(glob.attackers):
            glob.att_scores[i] = attacker.score
            glob.att_costs[i] = attacker.cost

    glob.current_run += 1

    if glob.current_run == glob.NUM_SIMS:
        nw.draw_network(N)
        draw_plot()