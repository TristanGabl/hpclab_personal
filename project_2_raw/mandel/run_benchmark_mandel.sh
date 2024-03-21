#!/bin/bash
#SBATCH --job-name=benchmark_mandel         # Job name    (default: sbatch)
#SBATCH --output=benchmark_mandel-%j.out    # Output file (default: slurm-%j.out)
#SBATCH --error=benchmark_mandel-%j.err     # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=1                      # Number of tasks
#SBATCH --cpus-per-task=32              # Number of CPUs per task
#SBATCH --constraint=EPYC_7763          # Select node with CPU
#SBATCH --mem-per-cpu=2048              # Memory per CPU
#SBATCH --time=00:15:00                 # Wall clock time limit

# load some modules & list loaded modules
module load gcc python
module list

# recompile
make clean
make

mkdir -p pngs

# run benchmark
python3 benchmark_mandel.py