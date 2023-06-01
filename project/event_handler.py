import simpy
import sys
import globals as glob
import network as nw
import attacker as att
import defender as defend


def generate_network():
    """
    Generates network according to selected network in GUI.
    """
    if glob.network_selection == "network1":
        return nw.create_basic_network(5, 3)
    if glob.network_selection == "network3":
        return nw.create_small_world(20, 4, 0.8)
    if glob.network_selection == "network2":
        return nw.create_power_law(20, 1, 0.4)

def generate_attackers(env, N):
    glob.attackers = []
    for id, attacker_settings in enumerate(glob.attacker_list):
        attacker  = att.Attacker(env, N, attacker_settings, id)
        glob.attackers.append(attacker)
        env.process(attacker.run())

def generate_defender(env, N):
    defender  = defend.Defender(env, N, glob.defender_strategy.get())
    env.process(defender.run())
    return defender

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

    """
    Create the Simpy enviroment and run it till one of termination criteria are
    triggered.
    """
    env = simpy.Environment()


    # Create attackers and defenders.
    generate_attackers(env, N)

    defender = generate_defender(env, N)

    # Run the simulation with multiple termination cireteria.
    env.run(until=glob.MAX_RUNTIME)

    glob.logger.info(f"Simulation ended at time: {env.now}")

    max_score, compromised_score = N.calculate_score()
    def_cost = defender.get_score()

    for i, attacker in enumerate(glob.attackers):
        print(f"Attacker {i} has score: {attacker.score}")

    print("Cost of defending actions:", def_cost)
    print("Sum of compromised score:", compromised_score)
    print("Max score:", max_score)

    print("Added costs and comprimised:", def_cost - compromised_score)

    nw.draw_network(N)