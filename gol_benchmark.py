import subprocess as sp
import numpy as np
import matplotlib
matplotlib.use("PS") #backend renderer
from matplotlib import pyplot as plt

test_sizes = ["128", "256", "512", "1024", "2048"]
tests = ["serial", "parallel", "collapse"]
num_threads = ["1", "2", "4", "8", "16", "32"]

#compile
for test in tests:
    sp.run(["gcc", "-fopenmp", "gol_"+test+".c", "-o", "gol_"+test])

#benchmark imps
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
p1 = plt.bar(ind-width, real_time[0], width=width)
p2 = plt.bar(ind, real_time[1], width=width)
p3 = plt.bar(ind+width, real_time[2], width=width)
plt.title("Real Time vs Input Size")
plt.ylabel("Elapsed Time (s)")
plt.xlabel("Grid Dimension (cells)")
plt.xticks(ind, test_sizes)
plt.legend([p1[0], p2[0], p3[0]], tests)
plt.savefig("input_realtime.eps", bbox_inches="tight")
plt.clf()

#plot usertime
p1 = plt.bar(ind-width, user_time[0], width=width)
p2 = plt.bar(ind, user_time[1], width=width)
p3 = plt.bar(ind+width, user_time[2], width=width)
plt.title("User Time vs Input Size")
plt.ylabel("Equivalent Time (s)")
plt.xlabel("Grid Dimension (cells)")
plt.xticks(ind, test_sizes)
plt.legend([p1[0], p2[0], p3[0]], tests)
plt.savefig("input_usertime.eps", bbox_inches="tight")
plt.clf()

#benchmark cores
real_time = [0 for x in num_threads]
user_time = [0 for x in num_threads]
for n, num in enumerate(num_threads):
    for i in range(10):
        sub = sp.run(["/usr/bin/time", "-f", "%e %U", "./gol_parallel", "2048", num],
                stdout=sp.DEVNULL, stderr=sp.PIPE)
        output = sub.stderr.decode().strip().split()
        real_time[n] += float(output[0])
        user_time[n] += float(output[1])
    real_time[n] /= 10
    user_time[n] /= 10

ind = np.arange(len(num_threads))
width = 0.5

#plot realtime
p1 = plt.bar(ind, real_time, width=width)
plt.title("Real Time vs Threads")
plt.ylabel("Time Elapsed (s)")
plt.xlabel("Threads Created")
plt.xticks(ind, num_threads)
plt.savefig("threads_realtime.eps", bbox_inches="tight")
plt.clf()

#plot usertime
p1 = plt.bar(ind, user_time, width=width)
plt.title("User Time vs Threads")
plt.ylabel("Equivalent Time (s)")
plt.xlabel("Threads Created")
plt.xticks(ind, num_threads)
plt.savefig("threads_usertime.eps", bbox_inches="tight")
plt.clf()
