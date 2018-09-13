import subprocess as sp
import numpy as np
from matplotlib import pyplot as plt

test_sizes = ["128", "256", "512", "1024", "2048"]
tests = ["serial", "parallel"]

"""
#compile
sp.run(["gcc", "gol_serial.c", "-o", "gol_serial"])
sp.run(["gcc", "-fopenmp", "gol_parallel.c", "-o", "gol_parallel"])

#benchmark
real_time = [[0 for x in test_sizes] for y in tests]
user_time = [[0 for x in test_sizes] for y in tests]
for t, test in enumerate(tests):
    for s, size in enumerate(test_sizes):
        print(test+size)
        for i in range(10):
            sub = sp.run(["/usr/bin/time", "-f", "%e %U", "./gol_"+test, size],
                    stdout=sp.DEVNULL, stderr=sp.PIPE)
            output = sub.stderr.decode().strip().split()
            real_time[t][s] += float(output[0])
            user_time[t][s] += float(output[1])
        real_time[t][s] /= 10
        user_time[t][s] /= 10
print(real_time)
print(user_time)
"""

real_time = [[0.01, 0.05, 0.211, 0.892, 3.438], [0.012, 0.029, 0.067, 0.243, 0.973]]
user_time = [[0.01, 0.05, 0.211, 0.891, 3.436], [0.1, 0.223, 0.508, 1.717, 6.344]]

ind = np.arange(len(test_sizes))
width = 0.3

p1 = plt.bar(ind-width/2, real_time[0], width=width)
p2 = plt.bar(ind+width/2, real_time[1], width=width)
plt.title("Elapsed Real Time")
plt.ylabel("Time (s)")
plt.xlabel("Grid Dimension (cells)")
plt.xticks(ind, test_sizes)
plt.legend([p1[0], p2[0]], tests)
plt.savefig("realtime.png", bbox_inches="tight")
plt.cla()

p1 = plt.bar(ind-width/2, user_time[0], width=width)
p2 = plt.bar(ind+width/2, user_time[1], width=width)
plt.title("Equivalent User-mode Time")
plt.ylabel("Time (s)")
plt.xlabel("Grid Dimension (cells)")
plt.xticks(ind, test_sizes)
plt.legend([p1[0], p2[0]], tests)
plt.savefig("usertime.png", bbox_inches="tight")
plt.cla()
