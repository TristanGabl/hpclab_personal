import matplotlib
import matplotlib.pyplot as plt
import subprocess
from typing import List


def run(type: str, n_threads: int, n: int) -> float:
    # we call subprocess with the desired variables
    output = subprocess.check_output(
        [f"build/{type}", str(n)],
        env={"OMP_NUM_THREADS": str(n_threads)}
    ).decode("utf-8")

    
    # extract the time
    time = float(output.split()[-1])
    print(f"threads = {n_threads}; time = {time}")
    return time


def main():

    # set up axis
    threads = [1,2,4,8,16,32]
    N = [1000000, 10000000, 100000000]
    # loops
    types = ["quicksort_seq", "quicksort_omp"]

    iterations = 5

    time_seq_collection = []
    for n in N:
        time_seq = 0    
        for itr in range(iterations):
            time_seq += run(types[0], threads[0], n) / iterations
        time_seq_collection.append(time_seq)
    
    print(f"{time_seq_collection=}")
    
    speedup_collection = []
    for i,n in enumerate(N):
        speedups = []
        for n_threads in threads:
            time_par = 0
            for itr in range(iterations):
                time_par += run(types[1], n_threads, n) / iterations
            speedups.append(float("{:.5f}".format(time_seq_collection[i] / time_par )))
        plt.plot(threads, speedups, label=f"n = {n}")
        speedup_collection.append(speedups)
    
    plt.title(f"quicksort benchmark, min_size = 1000")
    plt.xlabel("threads")
    plt.ylabel("speedup")
    plt.savefig("quicksort_benchmark.png")      

    with open("quicksort_benchmark.data", 'w') as file:
        file.write("quicksort_benchmark.data\n")
        file.write(f"n = {n}\n")
        file.write(f"sequential time = {time_seq}s\n")
        file.write(f"*average speedup of {iterations} iterations*\n")
        row_str = '\t'.join(["threads","n = 10^6","n = 10^7", "n = 10^8"])
        file.write(row_str + '\n')
        for i in range(len(threads)):
            row_str = '\t\t'.join([str(threads[i]),str(speedup_collection[0][i]), str(speedup_collection[1][i]), str(speedup_collection[2][i])])  # Separate items with tabs
            file.write(row_str + '\n')  # Add newline after each row
    


if __name__ == "__main__":
    main()

