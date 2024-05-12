#!/bin/bash
#SBATCH --job-name=benchmark      # Job name    (default: sbatch)
#SBATCH --output=sbatch/benchmark_strong_one_node-%j.out # Output file (default: slurm-%j.out)
#SBATCH --error=sbatch/benchmark_strong_one_node-%j.err  # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=33                # Number of tasks
#SBATCH --constraint=EPYC_7763    # Select node with CPU
#SBATCH --time=01:00:00           # Wall clock time limit


# enter venv
source ../project05-env/bin/activate
# Load some modules & list loaded modules
module load gcc openmpi python

rm benchmark_strong_50.txt
rm benchmark_strong_100.txt

runs=10
warm_ups=1
for ntask in 50 100; do
    for ncores in {1..3}; do
        echo "Running $ntask tasks on $ncores cores, $runs times to get average"
        for j in $(seq 1 $warm_ups); do
            # extract time from output
            mpirun -np $ncores python manager_worker.py 4001 4001 $ntask
        done
        for j in $(seq 1 $runs); do
            # extract time from output
            time=$(mpirun -np $ncores python manager_worker.py 4001 4001 $ntask | grep "Run took" | awk '{print $3}')
            echo "$ncores $time" >> benchmark_strong_$ntask.txt
        done
    done
done
    
deactivate