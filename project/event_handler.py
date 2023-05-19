import simpy
import sys
import globals as glob
import network as nw
import attacker as att
import defender as defend


def generate_attackers(env, N):
    for attacker_settings in glob.attacker_list:
        attacker  = att.Attacker(env, N, attacker_settings)
        env.process(attacker.run())

def generate_defender(env, N):
    defender  = defend.Defender(env, N, "random")
    env.process(defender.run())


def stop_simulation():
    """
    Function which will stop the simulation.
    """
    sys.exit("Simulation was terminated by the user!")

def start_simulation():
    """
    Function which will start the simulation.
    """

    """
    Create network and attackers and defenders.
    """
    N = nw.create_basic_network(5, 3)
    # nw.draw_network(N)


    """
    Create the Simpy enviroment and run it till one of termination criteria are
    triggered.
    """
    env = simpy.Environment()

    generate_attackers(env, N)

    generate_defender(env, N)

    # Print/Access the event list
    print(env._queue)

    # Run the simulation with multiple termination cireteria.
    env.run(until=glob.MAX_RUMTIME)

    glob.logger.info(f"Simulation ended at time: {env.now}")


    """
    Log all events which have happened in the simulation.
    """
    for handler in glob.logger.handlers:
        handler.flush()


    nw.draw_network(N)