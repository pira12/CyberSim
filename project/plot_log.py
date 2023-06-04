
import matplotlib.pyplot as plt

f = open("test/score_log.txt", "r")
results = {}
times = {}

for x in f:
    words = x.split(" ")

    time = int(words[2])
    role = words[3]
    score = int(words[5])
    cost = words[8]
    cost = int(cost[:-1])

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

for participant in results.keys():
    plt.plot(times[participant], results[participant], label=participant)

plt.title("Score over time")
plt.xlabel("Timer")
plt.ylabel("Score")
plt.legend()
plt.show()
