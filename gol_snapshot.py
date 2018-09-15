import subprocess as sp
import matplotlib
matplotlib.use("PS") #backend renderer
from matplotlib import pyplot as plt

test_sizes = ["128", "256", "512", "1024", "2048"]
tests = ["serial", "parallel", "collapse"]

#compile
for test in tests:
    sp.run(["gcc", "-fopenmp", "gol_"+test+".c", "-o", "gol_"+test])

#run and capture snapshots
for test in tests:
    for size in test_sizes:
        with open(test+size+".out", "w") as file:
            sp.run(["./gol_"+test, size], stdout=file)

#plot snapshots
for test in tests:
    for size in test_sizes:
        with open(test+size+".out", "r") as file:
            #parse data to 3D float array
            data = [[[float(z) for z in list(y)] for y in x.split()] for x in file.read().strip().split("\n\n")]
            for step, state in enumerate(data):
                p1 = plt.imshow(state)
                p1.set_cmap("Greys")
                plt.title("GoL-"+size+"-"+test+" state at step "+str(step*10))
                plt.savefig(test+size+"_"+str(step*10)+".eps", bbox_inches="tight")

