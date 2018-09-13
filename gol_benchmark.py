import subprocess as sp
from matplotlib import pyplot

test_sizes = ["128", "256", "512", "1024", "2048"]
tests = ["serial", "parallel"]

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
