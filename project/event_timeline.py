import network as nw
import attacker as att
import defender as deff


def generate_attackers(strategy):
    """
    Generates an attacker with strategy.
    """
    attackers.append(att.Attacker(strategy))


def generate_defenders(strategy):
    """
    Generates an defender with strategy.
    """
    defenders.append(deff.Defender(strategy))


def run_sim(run_time):
    """Function which runs the simulation"""
    current_time = 0
    while(current_time < run_time):
        # Handle attacker moves
        for attacker in attackers:
            attacker.scan_network(nw.N)
            attacker.attack_nodes(nw.N)

        # Handle defender moves
        for defender in defenders:
            defender.scan_network(nw.N)
            defender.defend_nodes(nw.N)
            defender.mitigate_nodes(nw.N)

        current_time += 1


if __name__ == "__main__":
    # Declare global variables
    total_run_time = 30
    event_list = []
    attackers = []
    defenders = []

    # Generate attackers and defenders
    generate_attackers(1)
    generate_defenders(1)

    # Run the simulation and draw network
    run_sim(total_run_time)
    nw.draw_network()
