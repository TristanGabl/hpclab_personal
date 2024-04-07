#!/bin/bash
#SBATCH --job-name=mini_app      # Job name    (default: sbatch)
#SBATCH --output=build/mini_app-%j.out # Output file (default: slurm-%j.out)
#SBATCH --error=build/mini_app-%j.err  # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=1                # Number of tasks
#SBATCH --constraint=EPYC_7763    # Select node with CPU
#SBATCH --cpus-per-task=128       # Number of CPUs per task
#SBATCH --mem-per-cpu=1024        # Memory per CPU
#SBATCH --time=00:05:00           # Wall clock time limit

# Load some modules & list loaded modules
module load gcc

make clean
make


export OMP_NUM_THREADS=64
build/main 128 100 0.005
