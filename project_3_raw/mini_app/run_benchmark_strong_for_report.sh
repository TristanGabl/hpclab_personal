#!/bin/bash
#SBATCH --job-name=benchmark_strong      # Job name    (default: sbatch)
#SBATCH --output=build/benchmark_strong-%j.out # Output file (default: slurm-%j.out)
#SBATCH --error=build/benchmark_strong-%j.err  # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=1                # Number of tasks
#SBATCH --constraint=EPYC_7763    # Select node with CPU
#SBATCH --cpus-per-task=128       # Number of CPUs per task
#SBATCH --mem-per-cpu=1024        # Memory per CPU
#SBATCH --time=02:00:00           # Wall clock time limit

# Load some modules & list loaded modules
module load gcc
module load python

make clean
make

python benchmark_strong.py

