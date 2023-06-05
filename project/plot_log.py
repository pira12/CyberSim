import globals as glob
import matplotlib.pyplot as plt
import numpy as np

def draw_plot():
    plt.clf()
    f = open(f"score_log.txt", "r")
    results = {}
    times = {}

    for x in f:
        words = x.split(" ")

        time = float(words[2])
        role = words[3]
        score = float(words[5])
        cost = words[8]
        cost = float(cost[:-1])

        # The score is the damage for the defender.
        # The total score is how bad the attack went for the defender,
        # the lower the better.
        if role == "Defender":
            total_score = score + cost
        else:
            total_score = score - cost

        if role in results:
            results[role].append(total_score)
            times[role].append(time)
        else:
            results[role] = [total_score]
            times[role] = [time]

    # All the simualtions have the same length and thus the same number of
    # results and the same timesteps.
    numb_of_res = int(len(results["Defender"]) / glob.NUM_SIMS)
    all_time = times["Defender"][0:0 + numb_of_res]

    for participant in results.keys():
        # plt.plot(times[participant], results[participant], label=participant)
        res = []

        # Add all the results with the same place together.
        for i in range(0, len(results[participant]), numb_of_res):
            one_sim = results[participant][i:i + numb_of_res]

            if i == 0:
                res = one_sim
            else:
                res = np.add(res, one_sim)

        res = np.divide(res, glob.NUM_SIMS)
        plt.plot(all_time, res, label=participant)

    plt.title("Score over time")
    plt.xlabel("Timer")
    plt.ylabel("Score")
    plt.legend()
    plt.savefig(f"./{glob.OUT_FOLDERNAME}/Plot_fig.png", format="PNG")
