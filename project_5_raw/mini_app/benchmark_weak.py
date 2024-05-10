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

    # extract from second last row the time
    time = float(output.split()[-3])
    threads = int((output.split()[-8]).rstrip(","))
    print(f"type = {type}; np = {threads}; time = {time}")
    return time



def main():

    threads = [1,4]
    Ns = [[64,128], [256]]
    n_t = 100

    iterations = 2
    iterations_warm_up = 2

    for i,N in enumerate(Ns):
        plt.clf()
        for n_x in N:
            time_seq = 0
            for itr in range(iterations_warm_up):
                run(threads[0], N[0], n_t)
            for itr in range(iterations):
                time_seq += run(threads[0], N[0], n_t, type="open_mpi") / iterations

            efficiency  = [1.0]
            for i in range(1, len(threads)):
                times_par = []
                for itr in range(iterations_warm_up):
                    run(threads[i], N[i], n_t, type="open_mpi")
                for itr in range(iterations):
                    times_par.append(run(threads[i], N[i], n_t, type="open_mpi"))

                efficiency.append(time_seq * iterations / sum(times_par))

            plt.plot(threads, efficiency)

            plt.xlabel("threads")
            plt.ylabel("efficiency")
            plt.savefig("mini_app_benchmark_weak.png")



if __name__ == "__main__":
    main()

