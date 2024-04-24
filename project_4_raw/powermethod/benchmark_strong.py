import matplotlib
import matplotlib.pyplot as plt
import subprocess
from typing import List
import os


def run(np: int, n_x: int, n_t: int) -> float:
    # we call subprocess with the desired variables
    # mpirun -np np ./powermethod_rows 3 n_x n_t -1e-6
    output = subprocess.check_output(
        ["mpirun", "-np", f"{np}", "./powermethod_rows", "3", f"{n_x}", f"{n_t}", "-1e-6"],
    ).decode("utf-8")
    
    # extract the time
    time = float(output.split()[-2])
    threads = int((output.split()[-6]).rstrip(","))
    print(f"np = {threads}; time = {time}")
    return time


def main():

    threads = [1,2,4,8,16,32,64]
    n_x = 10000
    n_t = 3000

    iterations = 10
    iterations_warm_up = 2
    
    time_seq = 0
    for itr in range(iterations_warm_up):
        run(threads[0], n_x, n_t)
    for itr in range(iterations):
        time_seq += run(threads[0], n_x, n_t) / iterations
    
    speedups = [1.0]
    for n_threads in threads[1:]:
        times_par = []
        for itr in range(iterations_warm_up):
            run(n_threads, n_x, n_t)
        for itr in range(iterations):
            times_par.append(run(n_threads, n_x, n_t))

        mean = time_seq * iterations / sum(times_par)
        speedups.append(mean)

    plt.plot(threads, speedups, label=f"n = {n_x}")
    
    plt.xlabel("threads")
    plt.ylabel("speedup")
    plt.legend()

    # get environment variable "ONE_MANY_NODE" to decide where to save the plot
    if os.environ.get("ONE_MANY_NODE") == "one_node":
        plt.savefig("powermethod_benchmark_strong_one_node.png")
    elif os.environ.get("ONE_MANY_NODE") == "many_nodes":
        plt.savefig("powermethod_benchmark_strong_many_nodes.png")
    else:
        plt.savefig("powermethod_benchmark_strong_one_node.png")


if __name__ == "__main__":
    main()

