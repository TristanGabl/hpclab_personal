#!/bin/bash
#SBATCH --job-name=benchmark_weak_pi         # Job name    (default: sbatch)
#SBATCH --output=benchmark_weak_pi-%j.out    # Output file (default: slurm-%j.out)
#SBATCH --error=benchmark_weak_pi-%j.err     # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=1                      # Number of tasks
#SBATCH --cpus-per-task=32              # Number of CPUs per task
#SBATCH --constraint=EPYC_7763          # Select node with CPU
#SBATCH --mem-per-cpu=2048              # Memory per CPU
#SBATCH --time=00:05:00                 # Wall clock time limit

# load some modules & list loaded modules
module load gcc python
module list

# recompile
make clean
make

# run benchmark
python3 benchmark_weak.py