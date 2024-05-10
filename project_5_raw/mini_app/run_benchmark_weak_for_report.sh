#!/bin/bash
#SBATCH --job-name=benchmark_weak      # Job name    (default: sbatch)
#SBATCH --output=build/benchmark_weak-%j.out # Output file (default: slurm-%j.out)
#SBATCH --error=build/benchmark_weak-%j.err  # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=64                # Number of tasks
#SBATCH --constraint=EPYC_7763    # Select node with CPU
#SBATCH --cpus-per-task=1      # Number of CPUs per task
#SBATCH --mem-per-cpu=1024        # Memory per CPU
#SBATCH --time=12:00:00           # Wall clock time limit

# Load some modules & list loaded modules
module load gcc
module load openmpi
module load python


python benchmark_weak.py

