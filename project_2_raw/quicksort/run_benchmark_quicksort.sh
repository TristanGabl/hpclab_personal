#!/bin/bash
#SBATCH --job-name=benchmark_quicksort         # Job name    (default: sbatch)
#SBATCH --output=benchmark_quicksort-%j.out    # Output file (default: slurm-%j.out)
#SBATCH --error=benchmark_quicksort-%j.err     # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=1                      # Number of tasks
#SBATCH --cpus-per-task=32              # Number of CPUs per task
#SBATCH --constraint=EPYC_7763          # Select node with CPU
#SBATCH --mem-per-cpu=1024              # Memory per CPU
#SBATCH --time=00:30:00                 # Wall clock time limit

# load some modules & list loaded modules
module load gcc python
module list

# recompile
make clean
make

# run benchmark
python3 benchmark_quicksort.py