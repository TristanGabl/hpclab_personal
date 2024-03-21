import matplotlib
import matplotlib.pyplot as plt
import subprocess
from typing import List


def run(type: str, n_threads: int, n: int) -> float:
    # we call subprocess with the desired variables
    output = subprocess.check_output(
        [f"./{type}", str(n)],
        env={"OMP_NUM_THREADS": str(n_threads)}
    ).decode("utf-8")
    
    # extract the time
    time = float(output.split()[-2])
    return time


def main():

    # set up axis
    threads = [1,2,4,8,12,16,24,32]
    plt.yscale("log")    

    # loops
    N_base = 1000000 # 10^6
    iterations = 10
    types = ["pi_omp_critical", "pi_omp_reduction"]
    time_serial = 0
    for itr in range(iterations):
        time_serial += run("pi_serial", 1, N_base) / iterations
    
    times_collection = []
    for current_type in types:
        times = []
        for n_threads in threads:
            time_parallel = 0
            for itr in range(iterations): 
                time_parallel += run(current_type, n_threads, n_threads * N_base) / iterations
            times.append(time_serial / time_parallel) #efficiency 
        plt.plot(threads, times, label=current_type, linewidth=1)
        times_collection.append(times)    
    
    plt.title("pi benchmark, weak scaling, N_per_thread = 1000000")
    plt.legend(loc="upper right")
    plt.xlabel("threads")
    plt.ylabel("efficiency")

    plt.savefig("benchmark_weak.png")      

    with open("benchmark_weak.data", 'w') as file:
        row_str = '\t'.join(["benchmark_weak", f"N = {N_base}"])
        file.write(row_str + '\n')
        file.write("efficiency:" + '\n')
        row_str = '\t'.join(["threads", "critical", "reduction"])
        file.write(row_str + '\n')
        for i in range(len(threads)):
            row_str = '\t'.join([str(threads[i]),str(times_collection[0][i]), str(times_collection[1][i])])  # Separate items with tabs
            file.write(row_str + '\n')  # Add newline after each row
    


if __name__ == "__main__":
    main()

