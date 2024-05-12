#!/bin/bash
#SBATCH --job-name=benchmark      # Job name    (default: sbatch)
#SBATCH --output=sbatch/benchmark_strong_one_node-%j.out # Output file (default: slurm-%j.out)
#SBATCH --error=sbatch/benchmark_strong_one_node-%j.err  # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=33                # Number of tasks
#SBATCH --nodes=1                 # Number of nodes
#SBATCH --ntasks-per-node=1       # Number of tasks per node
#SBATCH --constraint=EPYC_7763    # Select node with CPU
#SBATCH --cpus-per-task=1       # Number of CPUs per task
#SBATCH --mem-per-cpu=1024        # Memory per CPU
#SBATCH --time=10:00:00           # Wall clock time limit

# Load some modules & list loaded modules
module load gcc openmpi python

# enter venv
source ../project05-env/bin/activate

runs=2
for task in 50 100; do
    for ncores in {1..3}; do
        echo "Running $task tasks on $ncores cores, $runs times to get average"
        for j in $(seq 1 $runs); do
            # extract time from output
            output = $(mpirun -np $ncores python3 manager_worker.py 4001 4001 $task)
            time=$($output | grep "Run took" | awk '{print $3}')
            real_ncores=$(echo $output | grep "Run took" | awk '{print $6}')
            echo "$real_ncores $time" >> benchmark_strong_$task.txt
        done
    done
    
deactivate