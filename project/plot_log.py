
import matplotlib.pyplot as plt

f = open("test/log.txt", "r")
results = {}
times = {}

for x in f:
    words = x.split(" ")
    if len(words) < 4:
        continue

    score = words[-1]
    score = score[:-1]
    role = words[-2]
    time = words[-4]
    time = time[:-1]

    if words[-3] == "Score":
        if role in results:
            results[role].append(int(score))
            times[role].append(int(time))
        else:
            results[role] = [int(score)]
            times[role] = [int(time)]

for participant in results.keys():
    plt.plot(times[participant], results[participant], '*', label=participant)

plt.title("Score over time")
plt.xlabel("Timer")
plt.ylabel("Score")
plt.legend()
plt.show()
