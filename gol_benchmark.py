import subprocess as sp
import numpy as np
import matplotlib
matplotlib.use("Agg") #backend renderer
from matplotlib import pyplot as plt

test_sizes = ["128", "256", "512", "1024", "2048"]
tests = ["serial", "parallel", "collapse"]

#compile
for test in tests:
    sp.run(["gcc", "-fopenmp", "gol_"+test+".c", "-o", "gol_"+test])

#benchmark
real_time = [[0 for x in test_sizes] for y in tests]
user_time = [[0 for x in test_sizes] for y in tests]
for t, test in enumerate(tests):
    for s, size in enumerate(test_sizes):
        for i in range(10):
            sub = sp.run(["/usr/bin/time", "-f", "%e %U", "./gol_"+test, size],
                    stdout=sp.DEVNULL, stderr=sp.PIPE)
            output = sub.stderr.decode().strip().split()
            real_time[t][s] += float(output[0])
            user_time[t][s] += float(output[1])
        real_time[t][s] /= 10
        user_time[t][s] /= 10

ind = np.arange(len(test_sizes))
width = 0.3

#plot realtime
p1 = plt.bar(ind-width/2, real_time[0], width=width)
p2 = plt.bar(ind+width/2, real_time[1], width=width)
plt.title("Elapsed Real Time")
plt.ylabel("Time (s)")
plt.xlabel("Grid Dimension (cells)")
plt.xticks(ind, test_sizes)
plt.legend([p1[0], p2[0]], tests)
plt.savefig("realtime.png", bbox_inches="tight")
plt.clf()

#plot usertime
p1 = plt.bar(ind-width/2, user_time[0], width=width)
p2 = plt.bar(ind+width/2, user_time[1], width=width)
plt.title("Equivalent User-mode Time")
plt.ylabel("Time (s)")
plt.xlabel("Grid Dimension (cells)")
plt.xticks(ind, test_sizes)
plt.legend([p1[0], p2[0]], tests)
plt.savefig("usertime.png", bbox_inches="tight")
plt.clf()
