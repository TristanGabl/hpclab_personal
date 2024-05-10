import matplotlib
import matplotlib.pyplot as plt
import subprocess
from typing import List


def run(n_threads: int, n_x: int, n_t: int, type: str) -> float:
    # we call subprocess with the desired variables
    if type == "open_mpi":
        output = subprocess.check_output(
            ["mpirun", "-np", f"{n_threads}", "./build/main", f"{n_x}", f"{n_t}", "0.005"]
        ).decode("utf-8")
    elif type == "open_mp":
        output = subprocess.check_output(
            ["./build/main_openmp", f"{n_x}", f"{n_t}", "0.005"],
            env={"OMP_NUM_THREADS": str(n_threads)}
        ).decode("utf-8")

    # extract from second last row the time
    time = float(output.split()[-3])
    threads = int((output.split()[-8]).rstrip(","))
    print(f"type = {type}; np = {threads}; time = {time}")
    return time


def main():

    threads = [1,2,4]
    Ns = [[64,128], [256]]
    n_t = 100

    colors = ["blue", "orange", "green", "red", "purple", "brown", "pink", "gray", "olive", "cyan"]
    color_count = 0

    iterations = 2
    iterations_warm_up = 1

    for i,N in enumerate(Ns):
        # clear plot
        plt.clf()
        for n_x in N:
            time_seq = 0
            for itr in range(iterations_warm_up):
                run(threads[0], n_x, n_t, type="open_mpi")
            for itr in range(iterations):
                time_seq += run(threads[0], n_x, n_t, type="open_mpi") / iterations
            
            speedups = [1.0]
            upper_bound = [0.0]
            lower_bound = [0.0]
            for n_threads in threads[1:]:
                times_par = []
                for itr in range(iterations_warm_up):
                    run(n_threads, n_x, n_t, type="open_mpi")
                for itr in range(iterations):
                    times_par.append(run(n_threads, n_x, n_t, type="open_mpi"))

                mean = time_seq * iterations / sum(times_par)
                speedups.append(mean)
                # remove outliers if time is more than 3 times away from the mean (i know this is not scientificly correct, but the confidence interval is crazy big otherwise)
                times_par = [time for time in times_par if abs(time - mean) < 3 * mean]
                variance = sum((x - mean) ** 2 for x in times_par) / iterations
                std_dev = variance ** 0.5
                # use 90% confidence interval
                upper_bound.append(mean + 1.645 * std_dev)
                lower_bound.append(mean - 1.645 * std_dev)

            plt.plot(threads, speedups, label=f"open_mpi, n_x = {n_x}", color=colors[color_count])
            plt.fill_between(threads, lower_bound, upper_bound, color=colors[color_count], alpha=.15)
            color_count += 1

            for n_x in N:
                time_seq = 0
                for itr in range(iterations_warm_up):
                    run(threads[0], n_x, n_t, type="open_mp")
                for itr in range(iterations):
                    time_seq += run(threads[0], n_x, n_t, type="open_mp") / iterations
                
                speedups = [1.0]
                upper_bound = [0.0]
                lower_bound = [0.0]
                for n_threads in threads[1:]:
                    times_par = []
                    for itr in range(iterations_warm_up):
                        run(n_threads, n_x, n_t, type="open_mp")
                    for itr in range(iterations):
                        times_par.append(run(n_threads, n_x, n_t, type="open_mp"))

                    mean = time_seq * iterations / sum(times_par)
                    speedups.append(mean)
                    # remove outliers if time is more than 3 times away from the mean (i know this is not scientificly correct, but the confidence interval is crazy big otherwise)
                    times_par = [time for time in times_par if abs(time - mean) < 3 * mean]
                    variance = sum((x - mean) ** 2 for x in times_par) / iterations
                    std_dev = variance ** 0.5
                    # use 90% confidence interval
                    upper_bound.append(mean + 1.645 * std_dev)
                    lower_bound.append(mean - 1.645 * std_dev)
                    
            plt.plot(threads, speedups, label=f"open_mp, n_x = {n_x}", color=colors[color_count])
            plt.fill_between(threads, lower_bound, upper_bound, color=colors[color_count], alpha=.15)
            color_count += 1


        plt.xlabel("threads")
        plt.ylabel("speedup")
        plt.legend()
        if i == 0:
            plt.savefig("mini_app_benchmark_strong_64-256.png")
        elif i == 1:
            plt.savefig("mini_app_benchmark_strong_512-1024.png")
    


if __name__ == "__main__":
    main()

