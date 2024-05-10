import matplotlib
import matplotlib.pyplot as plt
import subprocess
from typing import List


def run(n_threads: int, n_x: int, n_t: int) -> float:
    # we call subprocess with the desired variables
    
    output = subprocess.check_output(
        ["mpirun", "-np", f"{n_threads}", "./build/main", f"{n_x}", f"{n_t}", "0.005"]
    ).decode("utf-8")

    # extract from second last row the time
    time = float(output.split()[-3])
    threads = int((output.split()[-8]).rstrip(","))
    print(f"np = {threads}; time = {time}")
    return time


def main():

    threads = [1,2,4,8,16]
    Ns = [[64,128,256],[512,1024]]
    n_t = 100

    colors = ["blue", "orange", "green", "red", "purple", "brown", "pink", "gray", "olive", "cyan"]
    color_count = 0

    iterations = 7
    iterations_warm_up = 2

    for i,N in enumerate(Ns):
        plt.clf()
        for n_x in N:
            time_seq_runs = []
            for itr in range(iterations_warm_up):
                run(threads[0], n_x, n_t)
            for itr in range(iterations):
                time_seq_runs.append(run(threads[0], n_x, n_t))
            
            time_seq_mean = sum(time_seq_runs) / len(time_seq_runs)
            # remove elements that are 4 times slower than the mean (outliers)
            time_seq_runs = [x for x in time_seq_runs if x < 4 * time_seq_mean]
            time_seq = sum(time_seq_runs) / len(time_seq_runs)
            
            speedups = [1.0]
            upper_bound = [1.0]
            lower_bound = [1.0]
            for n_threads in threads[1:]:
                times_par = []
                for itr in range(iterations_warm_up):
                    run(n_threads, n_x, n_t)
                for itr in range(iterations):
                    times_par.append(run(n_threads, n_x, n_t))

                mean_time = sum(times_par) / len(times_par)
                # remove elements that are 4 times slower than the mean (outliers)
                times_par = [x for x in times_par if x < 4 * mean_time]
                mean_speedup = time_seq * len(times_par) / sum(times_par)
                speedups.append(mean_speedup)
                variance = sum((x - mean_speedup) ** 2 for x in times_par) / len(times_par)
                std_dev = variance ** 0.5
                # use 90% confidence interval
                upper_bound.append(mean_speedup + 1.645 * std_dev)
                lower_bound.append(mean_speedup - 1.645 * std_dev)

            plt.plot(threads, speedups, label=f"n_x = {n_x}", color=colors[color_count])
            plt.fill_between(threads, lower_bound, upper_bound, color=colors[color_count], alpha=.15)
            color_count += 1


        plt.xlabel("threads")
        plt.ylabel("speedup")
        plt.legend()
        if i == 0:
            plt.savefig("mini_app_openMPI_benchmark_strong_64-256.png")
        elif i == 1:
            plt.savefig("mini_app_openMPI_benchmark_strong_512-1024.png")
    


if __name__ == "__main__":
    main()

