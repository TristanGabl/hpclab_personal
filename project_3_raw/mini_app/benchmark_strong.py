import matplotlib
import matplotlib.pyplot as plt
import subprocess
from typing import List


def run(n_threads: int, n_x: int, n_t: int) -> float:
    # we call subprocess with the desired variables
    output = subprocess.check_output(
        ["build/main", f"{n_x}", f"{n_t}", "0.005"],
        env={"OMP_NUM_THREADS": str(n_threads)}
    ).decode("utf-8")

    
    # extract the time
    time = float(output.split()[-3])
    threads = int((output.split()[-8]).rstrip(","))
    print(f"threads = {threads}; time = {time}")
    return time


def main():

    threads = [1,2,4,8,16]
    #N = [64,128,256]
    N = [512,1024]
    n_t = 100

    iterations = 10
    iterations_warm_up = 2

    for n_x in N:
        time_seq = 0
        for itr in range(iterations_warm_up):
            run(threads[0], n_x, n_t)
        for itr in range(iterations):
            time_seq += run(threads[0], n_x, n_t) / iterations
        
        speedups = [1.0]
        # upper_bound = [0.0]
        # lower_bound = [0.0]
        for n_threads in threads[1:]:
            times_par = []
            for itr in range(iterations_warm_up):
                run(n_threads, n_x, n_t)
            for itr in range(iterations):
                times_par.append(run(n_threads, n_x, n_t))

            mean = time_seq * iterations / sum(times_par)
            speedups.append(mean)
            # variance = sum((x - mean) ** 2 for x in times_par) / iterations
            # std_dev = variance ** 0.5
            # upper_bound.append(mean + 1.282 * std_dev)
            # lower_bound.append(mean - 1.282 * std_dev)

        plt.plot(threads, speedups, label=f"n_x = {n_x}")
        # plt.fill_between(threads, lower_bound, upper_bound, color='grey', alpha=.15)

        
    
    plt.xlabel("threads")
    plt.ylabel("speedup")
    plt.legend()
    plt.savefig("mini_app_benchmark_strong.png")
    


if __name__ == "__main__":
    main()

