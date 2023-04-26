import simpy
import logging
import globals

"""
Define logging settings.
"""
logging.basicConfig(filename='log.txt', filemode='w',
                    format='%(asctime)s %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


"""
Create the Simpy enviroment and run it till one of termination criteria are
triggered.
"""
env = simpy.Environment()

# Print/Access the event list
print(env._queue)

def termination_criteria1(env):
    if env.now >= globals.MAX_RUMTIME:
        return True
    return False

def termination_criteria2(env):
    if len(env._queue) == 0:
        return True
    return False

# Run the simulation with multiple termination cireteria.
env.run(until=globals.MAX_RUMTIME)

print("Simulation ended at time:", env.now)


"""
Log all events which have happened in the simulation.
"""
for handler in logger.handlers:
    handler.flush()