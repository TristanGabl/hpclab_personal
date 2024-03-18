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
    types = ["pi_omp_critical", "pi_omp_reduction"]
    time_serial = run("pi_serial", 1, 1000000000)
    times = [time_serial, time_serial, time_serial, time_serial, time_serial, time_serial, time_serial, time_serial]

    times_collection = []
    times_collection.append(times)

    plt.plot(threads, times, label="pi_serial", linewidth=1)

    for current_type in types:
        times = []
        for n_threads in threads:
            times.append(run(current_type, n_threads, 1000000000))
        plt.plot(threads, times, label=current_type, linewidth=1)
        times_collection.append(times)    
    
    plt.title("pi benchmark, strong scaling, N = 1000000000")
    plt.legend(loc="upper right")
    plt.xlabel("threads")
    plt.ylabel("seconds")

    plt.savefig("benchmark_strong.png")      

    with open("benchmark_strong.data", 'w') as file:
        row_str = '\t'.join(["serial", "critical", "reduction"])
        file.write(row_str + '\n')
        for i in range(len(threads)):
            row_str = '\t'.join([str(times_collection[0][i]), str(times_collection[1][i]), str(times_collection[2][i])])  # Separate items with tabs
            file.write(row_str + '\n')  # Add newline after each row
    


if __name__ == "__main__":
    main()

