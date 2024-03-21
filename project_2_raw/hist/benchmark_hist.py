import matplotlib
import matplotlib.pyplot as plt
import subprocess
from typing import List


def run(type: str, n_threads: int) -> float:
    # we call subprocess with the desired variables
    output = subprocess.check_output(
        [f"build/{type}"],
        env={"OMP_NUM_THREADS": str(n_threads)}
    ).decode("utf-8")

    
    # extract the time
    time = float(output.split()[-2])
    print(f"threads = {n_threads}; time = {time}")
    return time


def main():

    # set up axis
    threads = [1,2,4,8,16,32]
    # loops
    types = ["hist_seq", "hist_omp"]

    iterations = 10

    time_seq = 0
    for itr in range(iterations):
        time_seq += run(types[0], threads[0]) / iterations
    
    speedups = []
    for n_threads in threads:
        time_par = 0
        for itr in range(iterations):
            time_par += run(types[1], n_threads) / iterations
        speedups.append(float("{:.5f}".format(time_seq / time_par)))
    
    plt.plot(threads, speedups)
    plt.title("hist benchmark, vec_size = 1000000000")
    plt.xlabel("threads")
    plt.ylabel("speedup")
    plt.savefig("hist_benchmark.png")      

    with open("hist_benchmark.data", 'w') as file:
        file.write("hist_benchmark.data\n")
        file.write(f"sequential time = {time_seq}s\n")
        file.write(f"*average of {iterations} iterations*\n")
        row_str = '\t'.join(["threads","speedup"])
        file.write(row_str + '\n')
        for i in range(len(threads)):
            row_str = '\t\t'.join([str(threads[i]),str(speedups[i])])  # Separate items with tabs
            file.write(row_str + '\n')  # Add newline after each row
    


if __name__ == "__main__":
    main()

