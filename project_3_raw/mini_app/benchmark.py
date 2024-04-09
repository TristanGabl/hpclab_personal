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

    # set up axis
    threads = [1,2,4,8,16]
    n_x = 256
    n_t = 100
    # loops

    iterations = 3

    time_seq = 0
    for itr in range(iterations):
        time_seq += run(threads[0], n_x, n_t) / iterations
    
    speedups = [1.0]
    for n_threads in threads[1:]:
        time_par = 0
        for itr in range(iterations):
            time_par += run(n_threads, n_x, n_t) / iterations
        speedups.append(float("{:.6f}".format(time_seq / time_par)))
    
    print("--- benchmark done ---")
    
    plt.plot(threads, speedups)
    plt.xlabel("threads")
    plt.ylabel("speedup")
    plt.savefig("mini_app_benchmark.png")      

    with open("mini_app_benchmark.data", 'w') as file:
        file.write("mini_app_benchmark.data\n")
        file.write(f"sequential time = {time_seq}s\n")
        file.write(f"*average of {iterations} iterations*\n")
        row_str = '\t'.join(["threads","speedup"])
        file.write(row_str + '\n')
        for i in range(len(threads)):
            row_str = '\t\t'.join([str(threads[i]),str(speedups[i])])  # Separate items with tabs
            file.write(row_str + '\n')  # Add newline after each row
    print("--- data logging done ---")
    


if __name__ == "__main__":
    main()

