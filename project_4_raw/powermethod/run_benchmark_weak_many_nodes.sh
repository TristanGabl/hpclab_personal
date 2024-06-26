#!/bin/bash
#SBATCH --job-name=weak_many      # Job name    (default: sbatch)
#SBATCH --output=sbatch/benchmark_weak_many_nodes-%j.out # Output file (default: slurm-%j.out)
#SBATCH --error=sbatch/benchmark_weak_many_nodes-%j.err  # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=64                # Number of tasks
#SBATCH --nodes=64                 # Number of nodes
#SBATCH --ntasks-per-node=1       # Number of tasks per node
#SBATCH --constraint=EPYC_7763    # Select node with CPU
#SBATCH --cpus-per-task=1       # Number of CPUs per task
#SBATCH --mem-per-cpu=1500        # Memory per CPU
#SBATCH --time=10:00:00           # Wall clock time limit

# Load some modules & list loaded modules
module load gcc openmpi python

export ONE_MANY_NODE=many_nodes
python benchmark_weak.py
echo "run_benchmark_weak_many_nodes done!"

