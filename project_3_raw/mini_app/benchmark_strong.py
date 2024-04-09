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
    N = [64,128]#256,512,1024]
    n_t = 100

    iterations = 2
    iterations_warm_up = 0

    for n_x in N:
        time_seq = 0
        for itr in range(iterations_warm_up):
            run(threads[0], n_x, n_t)
        for itr in range(iterations):
            time_seq += run(threads[0], n_x, n_t) / iterations
        
        speedups = [1.0]
        for n_threads in threads[1:]:
            time_par = 0
            for itr in range(iterations_warm_up):
                run(n_threads, n_x, n_t)
            for itr in range(iterations):
                time_par += run(n_threads, n_x, n_t) / iterations
            speedups.append(float("{:.6f}".format(time_seq / time_par)))

        plt.plot(threads, speedups, label=f"n_x = {n_x}")
    
    plt.xlabel("threads")
    plt.ylabel("speedup")
    plt.legend()
    plt.savefig("mini_app_benchmark_strong.png")
    


if __name__ == "__main__":
    main()

