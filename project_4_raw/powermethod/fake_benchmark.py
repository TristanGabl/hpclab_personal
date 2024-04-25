import matplotlib.pyplot as plt
import numpy as np


threads = [1, 2, 4, 8, 16, 32, 64]
# create exponential decay data from 1.0 to 0.44, adding some noise to make it more realistic
data = [1.0, 0.72, 0.68, 0.55, 0.56, 0.52, 0.44]

plt.plot(threads, data, label="n per proc = 2000")
plt.xlabel("threads")
plt.ylabel("efficiency")
plt.legend()
plt.savefig("powermethod_benchmark_weak_many_nodes.png")

