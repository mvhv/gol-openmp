import subprocess
import sys
from matplotlib import pyplot
import time

test_sizes = ["128", "256", "512", "1024", "2048"]
tests = ["serial", "parallel"]

#compile
subprocess.run(["gcc", "gol_serial.c", "-o", "gol_serial"])
subprocess.run(["gcc", "-fopenmp", "gol_parallel.c", "-o", "gol_parallel"])

#run and capture snapshots
for test in tests:
    for size in test_sizes:
        with open(test+size+".out", "w") as file:
            subprocess.run(["./gol_"+test, size], stdout=file)

#plot snapshots
for test in tests:
    for size in test_sizes:
        with open(test+size+".out", "r") as file:
            #read file
            #remove final newline
            #split on empty lines
            #split on lines
            #remove newlines
            #split to chars
            #chars to floats
            data = [[[float(z) for z in list(y)] for y in x.split()] for x in file.read().strip().split("\n\n")]
            for step, state in enumerate(data):
                plot = pyplot.imshow(state)
                plot.set_cmap("Greys")
                pyplot.title("GoL-"+size+"-"+test+" state at step "+str(step*10))
                pyplot.savefig(test+size+"_"+str(step*10)+".png", bbox_inches="tight")
                pyplot.close()

