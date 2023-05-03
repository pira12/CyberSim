import simpy
import globals as glob
import network as nw
import attacker as att
import defender as defend

def termination_criteria1(env):
    if env.now >= globals.MAX_RUMTIME:
        return True
    return False

def termination_criteria2(env):
    if len(env._queue) == 0:
        return True
    return False

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

attacker1  = att.Attacker(env, N, glob.AttackStrat.RAND)
defender1  = defend.Defender(env, N, "random")

env.process(attacker1.run())
env.process(defender1.run())

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