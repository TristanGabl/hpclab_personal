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

    threads = [1,4,16,64]
    Ns = [[64,128,256,512],[128,256,512,1024],[256,512,1024,2048]]
    n_t = 100

    colors = ["blue", "orange", "green", "red", "purple", "brown", "pink", "gray", "olive", "cyan"]
    color_count = 0

    iterations = 7
    iterations_warm_up = 2

    for i,N in enumerate(Ns):
        
        time_seq_runs = []
        for itr in range(iterations_warm_up):
            run(threads[0], N[0], n_t)
        for itr in range(iterations):
            time_seq_runs.append(run(threads[0], N[0], n_t))

        time_seq_mean = sum(time_seq_runs) / len(time_seq_runs)
        # remove elements that are 4 times slower than the mean (outliers)
        time_seq_runs = [x for x in time_seq_runs if x < 4 * time_seq_mean]
        time_seq = sum(time_seq_runs) / len(time_seq_runs)

        efficiency  = [1.0]
        for j in range(1, len(threads)):
            times_par = []
            for itr in range(iterations_warm_up):
                run(threads[j], N[j], n_t)
            for itr in range(iterations):
                times_par.append(run(threads[j], N[j], n_t))
            
            times_par_mean = sum(times_par) / len(times_par)
            # remove elements that are 4 times slower than the mean (outliers)
            times_par = [x for x in times_par if x < 4 * times_par_mean]
            efficiency.append(time_seq * len(times_par) / sum(times_par))

        plt.plot(threads, efficiency, label=f"base n_x = {N[0]}", color=colors[color_count])
        color_count += 1

    plt.xlabel("threads")
    plt.ylabel("efficiency")
    plt.legend()
    
    plt.savefig("mini_app_openMPI_benchmark_weak.png")
        



if __name__ == "__main__":
    main()

