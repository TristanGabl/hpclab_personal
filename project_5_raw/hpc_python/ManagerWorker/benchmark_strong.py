import matplotlib
import matplotlib.pyplot as plt
import subprocess
from typing import List


def run(n_threads: int, n_x: int, n_y: int, ntasks: int) -> float:
    # we call subprocess with the desired variables
    

    # call main from manager_worker.py
    output = subprocess.check_output(["python", "manager_worker.py", str(n_x), str(n_y), str(ntasks), str(n_threads)], universal_newlines=True)

    # extract from second last row the time
    time = float(output.split()[-5])
    threads = int((output.split()[-2]))
    print(f"ntasks = {ntasks}; np = {threads}; time = {time}")
    return time


def main():

    threads = [1,2,4,8,12,16,24,32]
    number_tasks = [50,100]
    n_x = 4001
    n_y = 4001

    iterations = 2
    iterations_warm_up = 1


    for ntasks in number_tasks:
        time_seq_runs = []
        for itr in range(iterations_warm_up):
            run(threads[0], n_x, n_y, ntasks)
        for itr in range(iterations):
            time_seq_runs.append(run(threads[0], n_x, n_y, ntasks))
        
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
                run(n_threads, n_x, n_y, ntasks)
            for itr in range(iterations):
                times_par.append(run(n_threads, n_x, n_y, ntasks))

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

        plt.plot(threads, speedups, label=f"ntasks = {ntasks}")
        plt.fill_between(threads, lower_bound, upper_bound, alpha=.15)

        plt.xlabel("threads")
        plt.ylabel("speedup")
        plt.legend()
        plt.savefig("mandel_brot_strong_scaling_benchmark_python.png")
    


if __name__ == "__main__":
    main()

